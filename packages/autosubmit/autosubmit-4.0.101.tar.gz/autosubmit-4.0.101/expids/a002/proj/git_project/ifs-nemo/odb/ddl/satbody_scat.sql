//
//-- ODB/SQL file 'satbody_scat.sql'
//
//   Last updated:  15-DEC-2006
//

UPDATED;

SET $tslot = -1;

CREATE VIEW satbody_scat AS
  SELECT seqno  READONLY,         // r/o; MUST BECOME FIRST
         mpc@scatt_body,          // r/o
         azimuth@scatt_body,      // r/o
         incidence,               // r/o
         Kp,                      // r/o
         invresid,                // r/o
         dirskill,                // r/o
         Kp_qf@scatt_body,        // r/o
         sigma0_qf@scatt_body,    // r/o
         sigma0_sm@scatt_body,    // r/o
         soilmoist_sd@scatt_body, // r/o
         soilmoist_cf@scatt_body, // r/o
         soilmoist_pf@scatt_body, // r/o
         land_fraction@scatt_body,// r/o
         wetland_fraction@scatt_body,// r/o
         topo_complex@scatt_body,    // r/o

    FROM timeslot_index, index, hdr, sat, scatt, scatt_body
   WHERE obstype = $scatt
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
