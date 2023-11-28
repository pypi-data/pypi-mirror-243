CREATE VIEW ofb_7 AS
SELECT   
  expver                         as expver   ,    
  class                          as class    ,    
  stream                         as stream   ,    
  type                           as type     ,    
  andate                         as andate   ,    
  antime                         as antime   ,    
  reportype                      as reportype,    
  restricted                                 ,

  numtsl                     ,    

  timeslot                   ,

  seqno                      ,    
  groupid                    ,    
  obstype                    ,    
  codetype                   ,    
  sensor                     ,    
  date                       ,    
  time                       ,    
  rdbdate                                           ,
  rdbtime                                           ,
  report_status              ,    
  report_event1              ,    
  degrees(lat)               as lat@hdr                  ,    
  degrees(lon)               as lon@hdr                  ,    

  satellite_identifier       ,
  satellite_instrument@sat   ,
  zenith                     ,
  azimuth                    ,
  solar_zenith               ,
  solar_azimuth              ,

  entryno                    ,    
  obsvalue                   ,    
  varno                      ,    
  vertco_type                ,    
  vertco_reference_1         ,    

  datum_status               ,    
  datum_event1               ,    
  datum_anflag               ,
  biascorr                   ,    
  biascorr_fg                  ,    
  an_depar                   ,    
  fg_depar                   ,    
  datum_status_hires@update_1                        ,

  obs_error                  ,
  final_obs_error                  ,
  fg_error                   ,
  qc_pge                     ,
  vertco_reference_2, 
  an_sens_obs,
  report_rdbflag, 
  fc_sens_obs, 
  subtype, 
  datum_rdbflag, 
  mxup_traj, 
  hires@update_2, 
  bufrtype,

FROM desc, timeslot_index, hdr, sat, body, errstat, update_1, update_2
WHERE reportype is not null
AND groupid=7;
