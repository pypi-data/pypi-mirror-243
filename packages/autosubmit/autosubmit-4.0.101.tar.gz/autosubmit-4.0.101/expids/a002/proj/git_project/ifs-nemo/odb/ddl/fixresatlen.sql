//
//-- ODB/SQL file 'fixresatlen.sql'
//
//   New:  07-Mar-2006
//

CREATE VIEW fixresatlen
SELECT body.len, resat_averaging_kernel UPDATED // this fetches 3 columns: 1) body.len 
                           //                         2) resat_averaging_kernel.offset@resat
                           //                         3) resat_averaging_kernel.len@resat
FROM hdr, sat, resat
;
