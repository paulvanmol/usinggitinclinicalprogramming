/* Program: validate_sdtm_adam.sas
   Purpose: Minimal SDTM/ADaM structure checks for SAS 9.4 CI training.
   Study  : ABC-002
   Notes  : Training guardrail only; not full CDISC conformance validation.
*/
%if not %symexist(root) %then %let root=d:/workshop/training/ABC-002;
%let validation_failed=0;
%macro import_csv(path=, out=);
  %if %sysfunc(fileexist(&path)) %then %do;
    proc import datafile="&path" out=&out dbms=csv replace; guessingrows=max; run;
  %end;
  %else %do; %put ERROR: Expected source file not found: &path; %let validation_failed=1; %end;
%mend;
%macro require_vars(ds=, vars=);
  %local lib mem i var;
  %let lib=%upcase(%scan(&ds,1,.)); %let mem=%upcase(%scan(&ds,2,.));
  %do i=1 %to %sysfunc(countw(&vars));
    %let var=%upcase(%scan(&vars,&i));
    proc sql noprint; select count(*) into :_var_exists trimmed from dictionary.columns where libname="&lib" and memname="&mem" and upcase(name)="&var"; quit;
    %if &_var_exists=0 %then %do; %put ERROR: Required variable &var missing from &ds; %let validation_failed=1; %end;
  %end;
%mend;
%import_csv(path=&root/data/sdtm/csv/dm.csv, out=work.dm);
%import_csv(path=&root/data/sdtm/csv/ds.csv, out=work.ds);
%import_csv(path=&root/data/adam/csv/adsl.csv, out=work.adsl);
%if %sysfunc(exist(work.dm)) %then %require_vars(ds=work.dm, vars=STUDYID DOMAIN USUBJID SUBJID SEX RACE RFSTDTC ARMCD);
%if %sysfunc(exist(work.ds)) %then %require_vars(ds=work.ds, vars=STUDYID DOMAIN USUBJID DSSTDTC DSDECOD);
%if %sysfunc(exist(work.adsl)) %then %require_vars(ds=work.adsl, vars=STUDYID USUBJID SEX RACE ARMCD EOSSTT DCSREAS);
%if &validation_failed %then %do; %put ERROR: SDTM/ADaM validation failed.; %abort cancel; %end;
%else %put NOTE: SDTM/ADaM validation passed.;
