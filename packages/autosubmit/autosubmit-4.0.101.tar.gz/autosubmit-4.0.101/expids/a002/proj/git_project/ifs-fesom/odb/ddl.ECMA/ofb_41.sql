CREATE VIEW ofb_41 AS 

SELECT 

// Insert constant columns here 
expver@desc as expver, 
class@desc as class, 
stream@desc as stream, 
type@desc as type, 
andate@desc as andate, 
antime@desc as antime, 
reportype@hdr as reportype, 
numtsl@desc, 

// Insert hdr-aligned columns here 
date@hdr, 
rdbdate@hdr, 
lsm@modsurf, 
restricted@hdr, 
timeslot@timeslot_index, 
seqno@hdr, 
bufrtype@hdr, 
subtype@hdr, 
groupid@hdr, 
obstype@hdr, 
codetype@hdr, 
sensor@hdr, 
time@hdr, 
rdbtime@hdr, 
report_status@hdr, 
report_event1@hdr, 
report_rdbflag@hdr, 
degrees(lat@hdr) as lat@hdr, 
degrees(lon@hdr) as lon@hdr, 

// Insert body-aligned columns here 
entryno@body, 
vertco_reference_1@body, 
obsvalue@body, 
varno@body, 
vertco_type@body, 
datum_anflag@body, 
datum_status@body, 
datum_event1@body, 
datum_rdbflag@body, 
an_depar@surfbody_feedback, 
fg_depar@surfbody_feedback, 
snow_depth@surfbody_feedback, 
snow_density@surfbody_feedback, 
datum_status@surfbody_feedback, 
datum_sfc_event@surfbody_feedback, 
lsm@surfbody_feedback, 
datum_status_hires@update_1, 
obs_error@errstat, 
final_obs_error@errstat, 
fg_error@errstat, 
eda_spread@errstat

WHERE groupid@hdr == 41 ;
