//
//-- ODB/SQL file 'ssa_robody_2m.sql'
//
//   Last updated:  17-May-2002
//


READONLY;

CREATE VIEW ssa_robody_2m AS // SSA-analysis (2m analyses); ROBODY-part
  SELECT seqno,                      // r/o; Must become first
         entryno,
         varno,                      // r/o
         datum_status@surfbody_feedback UPDATED,       
         datum_sfc_event@surfbody_feedback UPDATED,        
         lsm@surfbody_feedback UPDATED,
         obsvalue ,           
         level@conv_body,                 // r/o
    FROM hdr, body, conv, conv_body, surfbody_feedback
   WHERE  ( (reportype >= 16001 AND reportype <= 16004 ) 
            OR  reportype == 16022 OR reportype == 16076  ) 
           AND ( varno  == 2 OR varno == 39 OR varno == 59 OR varno == 40
            OR varno == 29 OR varno == 58 ) 
;
