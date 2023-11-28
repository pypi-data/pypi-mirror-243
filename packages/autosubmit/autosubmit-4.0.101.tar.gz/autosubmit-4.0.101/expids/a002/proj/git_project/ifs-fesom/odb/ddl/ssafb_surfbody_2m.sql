//
//-- ODB/SQL file 'ssafb_surfbody_2m.sql'
//
//   Last updated:  17-May-2002
//


READONLY;

CREATE VIEW ssafb_surfbody_2m AS // SSA-analysis (2m analyses); ROBODY-part
  SELECT seqno,                      // r/o; Must become first
         entryno,
         varno,                      // r/o
         datum_status@surfbody_feedback UPDATED,        // possibly updated
         datum_sfc_event@surfbody_feedback UPDATED,        // possibly updated
         fg_depar@surfbody_feedback  UPDATED,          // possibly updated
         an_depar@surfbody_feedback  UPDATED,          // possibly updated
    FROM hdr, body,surfbody_feedback
   WHERE ( (reportype >= 16001 AND reportype <= 16004 ) 
      OR  reportype == 16022 OR reportype == 16076 )  
           AND ( varno  == 2 OR varno == 39 OR varno == 59 OR varno == 40
            OR varno == 29 OR varno == 58 ) 
;
