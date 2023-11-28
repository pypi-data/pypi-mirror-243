CREATE VIEW ofb_21 AS
SELECT   
  expver                         as expver   ,    
  class                          as class    ,    
  stream                         as stream   ,    
  type                           as type     ,    
  andate                         as andate   ,    
  antime                         as antime   ,    
  reportype                      as reportype,    
  restricted                                 ,

  numtsl                                      ,

  timeslot                                    ,

  seqno                                       ,
  bufrtype                                    ,
  subtype                                     ,
  groupid                                     ,
  obstype                                     ,
  codetype                                    ,
  sensor                                      ,
  date                                        ,
  time                                        ,
  rdbdate                                           ,
  rdbtime                                           ,
  report_status                               ,    
  report_event1                               ,    
  report_rdbflag                              ,    
  degrees(lat)           as lat@hdr           ,    
  degrees(lon)           as lon@hdr           ,    

  lsm                                         ,
  seaice                                      ,
  
  entryno                                     ,
  obsvalue                                    ,
  varno                                       ,
  vertco_type                                 ,
  vertco_reference_1                          ,

  datum_anflag                                ,    
  datum_status                                ,    
  datum_event1                                ,    
  datum_rdbflag                               ,    
  biascorr                                    ,
  biascorr_fg                                    ,
  qc_pge                                      ,
  an_depar                                    ,
  fg_depar                                    ,
  datum_status_hires@update_1                        ,

  obs_error                                   ,
  final_obs_error                                   ,
  fg_error                                    ,
  eda_spread                                  ,
  vertco_reference_2, 
  an_sens_obs, 
  satellite_identifier, 
  fc_sens_obs, 
  mxup_traj, 
  hires@update_2
FROM desc, timeslot_index, hdr, sat, modsurf, body, errstat, update_1, update_2
WHERE reportype is not null
AND groupid=21;
