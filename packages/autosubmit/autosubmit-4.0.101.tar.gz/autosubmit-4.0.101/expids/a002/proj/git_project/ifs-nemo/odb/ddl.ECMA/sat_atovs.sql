//
//-- ODB/SQL file 'sat_atovs.sql'
//
//   Last updated:  07-Jul-2018
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sat_atovs AS
  SELECT seqno  READONLY,                  // r/o; MUST BECOME FIRST
         cldcover READONLY,                // r/o; MUST BECOME FIRST
         skintemper,                       // possibly updated
         cldptop[1:3],                     // possibly updated
         cldne[1:3],                       // possibly updated
         skintemp[1:($NMXUPD+1)]@radiance, // possibly updated
         scatterindex_89_157 UPDATED,      // possibly updated
         scatterindex_23_89 UPDATED,       // possibly updated
         scatterindex_23_165 UPDATED,      // possibly updated
         lwp_obs UPDATED,                  // possibly updated
         t2m,
         typesurf UPDATED,
         surface_class,
         cldptop[1:3],                     // possibly updated
         cldne[1:3],                       // possibly updated
         scanpos@radiance  READONLY,       // r/o
         zenith@sat  READONLY,             // r/o
         azimuth@sat  READONLY,            // r/o
         solar_zenith@sat  READONLY,       // r/o
         solar_azimuth@sat  READONLY,      // r/o
         asr_pcloudy_high,                 // updated for overcast cloudy ir
         asr_pcloudy_middle  READONLY,     // r/o
    FROM timeslot_index, index, hdr, sat, radiance, modsurf
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $satem 
     AND codetype = $atovs
 ORDERBY seqno
;
