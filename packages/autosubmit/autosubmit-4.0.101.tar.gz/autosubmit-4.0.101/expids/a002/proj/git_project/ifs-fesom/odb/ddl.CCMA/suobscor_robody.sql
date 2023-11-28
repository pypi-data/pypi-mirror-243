//
//-- ODB/SQL file 'suobscor_robody.sql'
//
//   Last updated:  27-March-2006
//

UPDATED;


CREATE VIEW suobscor_robody AS   
  SELECT entryno, varno,     
         obs_corr_ev[1:$NUMEV],
         obs_corr_mask@errstat,
         obs_corr_diag[1:$NUMDIAG],   
         final_obs_error READONLY,
         obsvalue READONLY,
         vertco_reference_1 READONLY,
  FROM   index, hdr, body, errstat
;
