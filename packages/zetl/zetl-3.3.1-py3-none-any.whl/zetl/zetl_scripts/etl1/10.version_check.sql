/*
  -- Dave Skura, 2023
Use Global Variables = gblvar_rundate,gblvar_label
*/

SELECT 
	'Default connection sqlite '||sqlite_version() as dbversion
	,'SCRIPT{gblvar_label}' as label
	,SCRIPT{gblvar_rundate} as dtm
	;
