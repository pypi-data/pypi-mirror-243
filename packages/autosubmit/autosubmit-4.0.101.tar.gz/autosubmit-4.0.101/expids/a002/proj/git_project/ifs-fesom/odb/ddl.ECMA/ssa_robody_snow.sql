//
//-- ODB/SQL file 'ssa_robody_snow.sql'
//
//   Last updated:  17-May-2002
//


READONLY;

CREATE VIEW ssa_robody_snow AS // SSA-analysis (snow only); ROBODY-part
  SELECT seqno,                      // r/o; Must become first
         entryno,
         varno,                      // r/o
         datum_status@surfbody_feedback UPDATED,        
         datum_sfc_event@surfbody_feedback UPDATED,        
         lsm@surfbody_feedback UPDATED,
         obsvalue ,           
    FROM hdr, body, surfbody_feedback
   WHERE obstype= $imsims or
   (obstype = $synop AND ( codetype = $synop_land OR codetype = $synop_land_auto OR codetype = $add_land_surface OR codetype == 170 ))
;
