UPDATED;
CREATE VIEW aeolus_auxmet_update_hdrflag AS
    SELECT date@hdr READONLY,
           time@hdr READONLY, 
           retrtype@hdr READONLY,
           aeolus_hdrflag@aeolus_hdr 
     FROM hdr, aeolus_hdr
     WHERE retrtype@hdr=1
;

