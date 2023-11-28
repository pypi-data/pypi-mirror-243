//
//-- ODB/SQL file 'robody_tc.sql'
//
//   Last updated:  16-Oct-2001
//

CREATE VIEW robody_tc AS     // Time correlation; READONLYBODY-part
  SELECT datum_event1@body,        // possibly updated
         datum_status@body,        // possibly updated
         datum_anflag,             // possibly updated
         entryno  READONLY, varno  READONLY, // r/o
         qc_a,      // possibly updated
         qc_l,      // possibly updated
         qc_pge,      // possibly updated
         vertco_reference_1  READONLY,   // r/o
         final_obs_error  READONLY,// r/o
         fg_error         READONLY,// r/o
         actual_depar,  // use to store departure (massaged by qc)
         actual_ndbiascorr UPDATED,    // to pass actual bias correction from onse subroutine to another (work ODB column)
    FROM index, hdr, body, errstat
   WHERE obstype = $synop
      OR obstype = $dribu
;
