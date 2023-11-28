//
//-- ODB/SQL file 'obsdist_hdr2resat_averaging_kernel.sql'
//
//   Created:  22-Jun-2009
//

READONLY;

SET $pe = 0;
SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;
SET $hdr_min = -1;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW obsdist_hdr2resat_averaging_kernel AS
  SELECT distribid, seqno, window_offset
    FROM hdr, sat, resat, resat_averaging_kernel
       WHERE 1 <= distribid
       AND distribtype = 1

// the following are always true and needed in order to make sure that:

// (a) search order is preserved as in obsdist_hdr2body [-> NOREORDER]
// (b) tables "sat, resat, resat_averaging_kernel"  won't get ignored

     AND (#resat_averaging_kernel >= 1)

// (c) query doesn't return anything, when resat_averaging_kernel is in fact empty
//      (this is needed only during the transition period when ALIGNment
//       between body & resat_averaging_kernel may not be established/true)

     AND (resat_averaging_kernel.len@resat > 0)

// (d) data is *REALLY* resat-related (see obsdist_resat.sql)

     AND (obstype = $satem) AND (codetype = $resat)
       AND (obstype = $obstype OR $obstype = -1 )
       AND (codetype = $codetype OR $codetype = -1)
     AND (sensor = $sensor OR $sensor = -1)
     AND (window_offset = $hdr_min OR $hdr_min = -1)
     AND paral($pe, distribid)
;
