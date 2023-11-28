CREATE VIEW ofb_39 AS
SELECT   
  expver                         as expver   ,    
  class                          as class    ,    
  stream                         as stream   ,    
  type                           as type     ,    
  andate                         as andate   ,    
  antime                         as antime   ,    
  reportype                      as reportype,    
  restricted                                 ,

  mxup_traj                                    ,
  numtsl                                       ,

  timeslot                                     ,
  seqno                                        ,
  bufrtype                                     ,
  subtype                                      ,
  groupid                                      ,
  obstype                                      ,
  codetype                                     ,
  date                                         ,
  time                                         ,
  rdbdate                                           ,
  rdbtime                                           ,
  degrees(lat)           as lat@hdr            ,    
  degrees(lon)           as lon@hdr            ,    

  satellite_identifier                         ,

  entryno                                      ,
  obsvalue                                     ,
  varno                                        ,
  vertco_type                                  ,
  vertco_reference_1                           ,

  biascorr                                     ,
  an_depar                                     ,
  fg_depar                                     ,

  fc_sens_obs                                  ,
  an_sens_obs                                  ,
  obs_error                                    ,
  final_obs_error                              ,
  fg_error                                     ,
  datum_status_hires@update_1                  ,

FROM desc, timeslot_index, hdr, sat, body, errstat, update_1
WHERE reportype is not null
AND groupid=39;
