// BSD-2-Clause. stackdump: loaded with DYLD_INSERT_LIBRARIES; kill -USR2 <pid> writes the symbolised stack of every thread to stderr
// (the thread that takes the signal: backtrace(); the others: thread_get_state, then the frame-pointer chain, symbolised with dladdr).
#include <execinfo.h>
#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <dlfcn.h>
#include <mach/mach.h>
static void line(int i, unsigned long pc) {
	Dl_info d; char b[512];
	if (dladdr((void *)pc, &d) && d.dli_sname) snprintf(b, sizeof b, "  %2d %#lx %s`%s + %lu\n", i, pc, strrchr(d.dli_fname, '/') ? strrchr(d.dli_fname, '/') + 1 : d.dli_fname, d.dli_sname, pc - (unsigned long)d.dli_saddr);
	else snprintf(b, sizeof b, "  %2d %#lx ?\n", i, pc);
	write(2, b, strlen(b));
}
static void all(int s) {
	void *f[64]; int n = backtrace(f, 64); char b[128];
	write(2, "=== signalled thread\n", 21); for (int i = 0; i < n; i++) line(i, (unsigned long)f[i]);
	thread_act_array_t th; mach_msg_type_number_t nt = 0; mach_port_t self = mach_thread_self();
	if (task_threads(mach_task_self(), &th, &nt) != KERN_SUCCESS) return;
	for (unsigned t = 0; t < nt; t++) {
		if (th[t] == self) continue;
		x86_thread_state64_t st; mach_msg_type_number_t c = x86_THREAD_STATE64_COUNT;
		kern_return_t kr = thread_get_state(th[t], x86_THREAD_STATE64, (thread_state_t)&st, &c);
		snprintf(b, sizeof b, "=== thread port %#x: get_state %d rip %#llx rbp %#llx rsp %#llx\n", th[t], kr, st.__rip, st.__rbp, st.__rsp); write(2, b, strlen(b));
		if (kr != KERN_SUCCESS) continue;
		line(0, st.__rip);
		unsigned long *rsp = (unsigned long *)st.__rsp; line(1, rsp[0]);			/* in a trap stub the return address is at the top of the stack */
		unsigned long *fp = (unsigned long *)st.__rbp;
		for (int i = 2; i < 40 && fp && ((unsigned long)fp & 7) == 0; i++) { line(i, fp[1]); unsigned long *nfp = (unsigned long *)fp[0]; if (nfp <= fp) break; fp = nfp; }
	}
	(void)s;
}
__attribute__((constructor)) static void init(void) { signal(SIGUSR2, all); }
