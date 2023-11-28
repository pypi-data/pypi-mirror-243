//
//-- ODB/SQL file 'obsort_hdr2resat_averaging_kernel.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW obsort_hdr2resat_averaging_kernel AS
  SELECT target, seqno
    FROM index, hdr, sat, resat, body, resat_averaging_kernel
   WHERE (   ($all = 1)
          OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)

// the following are always true and needed in order to make sure that:

// (a) search order is preserved as in obsort_hdr2body [-> NOREORDER]
// (b) tables "sat, resat, resat_averaging_kernel"  won't get ignored

     AND (#resat_averaging_kernel >= 1)

// (c) query doesn't return anything, when resat_averaging_kernel is in fact empty
//      (this is needed only during the transition period when ALIGNment
//       between body & resat_averaging_kernel may not be established/true)

     AND (resat_averaging_kernel.len@resat > 0)

// (d) data is *REALLY* resat-related (see obsort_resat.sql)

     AND (obstype = $satem) AND (codetype = $resat)
     ORDERBY seqno
;
