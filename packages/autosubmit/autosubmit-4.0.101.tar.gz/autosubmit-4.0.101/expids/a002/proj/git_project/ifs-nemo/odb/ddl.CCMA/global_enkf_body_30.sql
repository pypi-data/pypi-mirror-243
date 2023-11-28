//
//-- ODB/SQL file 'global_enkf_30.sql'
//
//   Last updated:  
//   By          :  Anne Fouilloux

READONLY;

CREATE VIEW global_enkf_body_30 AS
  SELECT
    varno,    //body
    vertco_reference_1,  //body
    vertco_reference_2,  //body
    fg_depar,  //body
    an_depar  UPDATED,  //body
    biascorr_fg,  //body
    biascorr,  //body
    obs_error,  //errstat
    final_obs_error  UPDATED, //errstat
    qc_a,  //body
    qc_l,  //body
    qc_pge  UPDATED,  //body
    datum_anflag   UPDATED, //body
    datum_status   UPDATED, //body
    datum_event1   UPDATED, //body
    obsvalue, //body
    jacobian_peak,  //body
    jacobian_hpeak, //body
    hprior@enkf[1:min($NMXENKF,30)], //enkf
   FROM body,errstat, ensemble,enkf[1:min($NMXENKF,30)]
;

