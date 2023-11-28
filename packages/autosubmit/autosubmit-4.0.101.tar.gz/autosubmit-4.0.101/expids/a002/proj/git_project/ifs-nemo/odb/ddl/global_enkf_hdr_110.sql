//
//-- ODB/SQL file 'global_enkf_hdr_110.sql'
//
//   Last updated:  
//   By          :  Anne Fouilloux

READONLY;

CREATE VIEW global_enkf_hdr_110 AS
  SELECT
    seqno,  //hdr
    body.offset, //hdr
    body.len, //hdr
    lat,  //hdr
    lon,  //hdr
    date,  //hdr
    time,  //hdr
    obstype, //hdr
    codetype, //hdr
    reportype, //hdr
    stalt,  //hdr
    orography, //modsurf
    satellite_identifier, //sat
    sensor,  //hdr
   FROM hdr,sat,modsurf
;


