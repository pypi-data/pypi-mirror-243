//
//-- ODB/SQL file 'update_fcdiag_links.sql'
//
//   Last updated:  24/07/10
//   By          :  Anne Fouilloux

UPDATED;

CREATE VIEW update_fcdiag_links AS
  SELECT 
     body READONLY,         // r/o (offset + length)
    FROM hdr
;
