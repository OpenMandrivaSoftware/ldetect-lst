/* take xc/programs/Xserver/hw/xfree86/common/xf86PciInfo.h in XFree86-4 */
#include "xf86PciInfo.h"

const char *vendor2text(int id) {
  SymTabRec *p;
  for (p = xf86PCIVendorNameInfoData; p->token; p++)
    if (p->token == id) return p->name;
  fprintf(stderr, "error, bad vendor id\n");
  exit(1);
}

main() {
  pciVendorDeviceInfo *p;

  for (p = xf86PCIVendorInfoData; p->VendorID; p++) {
    struct pciDevice *q;
    const char *vendor = vendor2text(p->VendorID);
    for (q = p->Device; q->DeviceID; q++) {
      printf("0x%04x\t0x%04x\t\"unknown\"\t\"%s|%s\"\n", p->VendorID, q->DeviceID, vendor, q->DeviceName);
    }
  }
}
