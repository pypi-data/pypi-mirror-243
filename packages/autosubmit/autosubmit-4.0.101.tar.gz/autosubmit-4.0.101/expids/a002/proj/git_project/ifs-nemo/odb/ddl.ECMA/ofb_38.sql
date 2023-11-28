CREATE VIEW ofb_38 AS 

SELECT 

// Insert constant columns here 
expver@desc as expver, 
class@desc as class, 
stream@desc as stream, 
type@desc as type, 
andate@desc as andate, 
antime@desc as antime, 
reportype@hdr as reportype, 
mxup_traj@desc, 
numtsl@desc, 

// Insert hdr-aligned columns here 
date@hdr, 
rdbdate@hdr, 
restricted@hdr, 
timeslot@timeslot_index, 
seqno@hdr, 
bufrtype@hdr, 
subtype@hdr, 
groupid@hdr, 
obstype@hdr, 
codetype@hdr, 
time@hdr, 
rdbtime@hdr, 
degrees(lat@hdr) as lat@hdr, 
degrees(lon@hdr) as lon@hdr, 
satellite_identifier@sat, 
report_status@hdr, 
report_event1@hdr, 
report_event2@hdr, 
sensor@hdr, 

// Insert body-aligned columns here 
entryno@body, 
vertco_reference_1@body, 
obsvalue@body, 
varno@body, 
vertco_type@body, 
biascorr@body, 
an_depar@body, 
fg_depar@body, 
fc_sens_obs@body, 
an_sens_obs@body, 
obs_error@errstat, 
final_obs_error@errstat, 
fg_error@errstat, 
datum_status@body, 
datum_event1@body, 
datum_event2@body, 
datum_status_hires@update_1

WHERE groupid@hdr == 38 ;
