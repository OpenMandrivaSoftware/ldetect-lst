#include <stdio.h>

typedef struct {
    int			token;		/* id of the token */
    const char *	name;		/* token name */
} SymTabRec, *SymTabPtr;

#define CARD16 int

#define INIT_PCI_CARD_INFO
#define INIT_PCI_VENDOR_INFO
#define INIT_PCI_VENDOR_NAME_INFO
#define VENDOR_INCLUDE_NONVIDEO
