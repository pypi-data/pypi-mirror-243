CREATE VIEW odb2ee_aeolus_auxmet AS
    SELECT seqno@hdr,
lat@hdr, lon@hdr, lev@aeolus_auxmet,
ptop@aeolus_auxmet, pnom@aeolus_auxmet, ztop@aeolus_auxmet, znom@aeolus_auxmet, 
u@aeolus_auxmet, v@aeolus_auxmet, 
t@aeolus_auxmet, rh@aeolus_auxmet, 
q@aeolus_auxmet, cc@aeolus_auxmet, 
clwc@aeolus_auxmet, ciwc@aeolus_auxmet, 
timeslot@timeslot_index, timeslot@index, 
date@hdr, time@hdr, 
andate@desc, antime@desc, 
error_t@aeolus_auxmet, error_rh@aeolus_auxmet, error_p@aeolus_auxmet, 
aeolus_hdrflag@aeolus_hdr, 
retrtype@hdr
     FROM hdr, sat, aeolus_hdr, aeolus_auxmet, timeslot_index, index, desc
     WHERE retrtype@hdr=1
     ORDERBY date@hdr,time@hdr,aeolus_hdrflag@aeolus_hdr
;

