//
//-- ODB/SQL file 'setup_tovscv.sql'
//
//   Last updated:  05-Jul-2002
//

READONLY;

CREATE VIEW setup_tovscv AS
  SELECT seqno,timeslot,
// get obstype and obs characteristix for debugging purposes only
         obstype,
         codetype,
         instrument_type,
         retrtype,
         areatype,
// get abnob for debugging purposes only
	       abnob, 
         maptovscv,
         skintemper,
         skintemp[1:($NMXUPD+1)]@radiance UPDATED,
         tsfc,
   FROM  index, hdr, sat, radiance, modsurf
  WHERE  (obstype = $satem)
     AND (codetype = $atovs)
ORDERBY  timeslot, seqno
;
