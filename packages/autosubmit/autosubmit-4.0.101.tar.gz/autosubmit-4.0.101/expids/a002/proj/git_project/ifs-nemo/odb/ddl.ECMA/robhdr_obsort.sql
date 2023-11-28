//
//-- ODB/SQL file 'robhdr_obsort.sql'
//
//   Last updated:  17-May-2001
//

READONLY; // the view is treated as read/only

SET $all = 1;
SET $hdr_min =0; // here $hdr_min corresponds to distribtype 1 if on the model grid

CREATE VIEW robhdr_obsort AS
  SELECT lat, lon,                //  r/o
    FROM index, hdr
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1)
	  OR ($all = 2) )
      AND distribtype = $hdr_min
   ORDERBY sensor,distribid, gp_number

;
