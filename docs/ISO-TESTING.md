# Testing Mach-O programs on the pearOS ISO itself (2026-11-18)

The image has `darwinator.ko`, `machrun`, `open` and a kernel that fits the module, so it is the test machine (no separate lab VM needed). It runs under QEMU/KVM; ssh is switched on by a file on the EFI partition.

1. Take the ISO (`gh release download iso-latest -R pearOS-bsd/iso`, `xz -d`), copy it, and put your public key on its EFI partition as `ssh.enable` (the ESP is the first partition, 64 MB at byte 40960):
   `sudo mount -o loop,offset=40960,sizelimit=67108864 test.iso /mnt/esp; cat ~/.ssh/id.pub | sudo tee /mnt/esp/ssh.enable; sudo umount /mnt/esp`
   (sshd starts at boot only if this file is there; the key and the account `alex` / password `pear` both work.)
2. Start it with a network card and a forwarded port:
   `qemu-system-x86_64 -accel kvm -cpu host -m 6144 -smp 4 -machine q35 -vga std -display none -drive if=pflash,format=raw,readonly=on,file=OVMF_CODE_4M.fd -drive if=pflash,format=raw,file=vars.fd -drive if=none,id=u,file=test.iso,format=raw,snapshot=on -device ich9-ahci,id=ahci -device ide-hd,drive=u,bus=ahci.0,bootindex=1 -device qemu-xhci -device usb-kbd -device usb-tablet -netdev user,id=n0,hostfwd=tcp::2224-:22 -device virtio-net-pci,netdev=n0 -smbios type=1,product=wsbsd-ci -serial file:serial.log`
   `ssh -p 2224 alex@localhost` after about two and a half minutes. `sudo` needs the password (`echo pear | sudo -S -p "" ...`).
3. `sudo kldload darwinator` (it is not loaded by itself while `/sbin/launchd` is missing from the image). `sysctl kern.darwinator` lists the switches (`dyld`, `use_cache`, `debug`).
4. Build a Mach-O program on FreeBSD (`darwinator/tests/macho-toolchain/build.sh`, `objc/build.sh`; `ld64.lld` of the `llvm` package), `scp` it, run it: the kernel hands it to `machrun` (binmisc `macho64`).

Result of 2026-11-18 (ISO of run 12 of the iso workflow): the Objective-C program of `macho-toolchain/objc`, built on FreeBSD without any file of Apple's, prints `objc: Hello answer = 42` in the image through `machrun`.
Not tried: the real dyld path (`kern.darwinator.dyld=1`, needs the Mac's `/usr/lib/dyld` and frameworks, which are the owner's and not in the image) and `/open/AppKit`.
