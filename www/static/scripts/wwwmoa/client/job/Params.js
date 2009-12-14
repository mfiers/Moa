
dojo.provide("wwwmoa.client.job.Params");
dojo.require("dojo.string");


dojo.addOnLoad(function() {dojo.declare("wwwmoa.client.job.Params", null, {
		
		_params : null,

		setParams : function(iparams) {
		    this._params=iparams;
		},

		getParams : function() {
		    return this._params;
		},

		rewriteParam : function(name, values) {
		    for(var x=0; x<this._params.length; x++)
			if(this._params[x].name==name)
			    this._params[x].values=this.transValuesOTI(values, this._params[x].type);
		},

		getParamCount : function() {
		    if(dojo.isArray(this._params))
			return this._params.length;
		    
		    return 0;
		},

		getParam : function(locator) {
		    if(!dojo.isArray(this._params))
			return null;

		    if(dojo.isString(locator)) {
			for(var x=0; x<this._params.length; x++)
			    if(this._params[x].name==locator)
				return this._params[x];

			return null;
		    }

		    if((this._params.length>locator)&&(locator>=0))
			return this._params[locator];

		    return null;
		},
		   
		getParamNames : function() {
		    var names=[];

		    if(dojo.isArray(this._params))
			for(var x=0; x<this._params.length; x++)
			    names[x]=this._params[x].name;

		    return names;
		},

		getParamGroups : function() {
		    var groups=[];
		    var groups_unique=[];

		    if(dojo.isArray(this._params))
			for(var x=0; x<this._params.length; x++)
			    groups[x]=this._params[x].group;

		    groups.sort();
		    
		    var y=0;

		    for(var x=0; x<groups.length; x++) {
			if((y==0) || (groups[x]!=groups_unique[y-1])) {
			    groups_unique[y]=groups[x];
			    y++;
			}
		    }

		    return groups_unique;
		},

		getParamsByGroup : function(igroup) {
		    var iparams=[];

		    for(var x=0; x<this._params.length; x++) {
			if(this._params[x].group==igroup)
			    iparams.push(this._params[x]);
		    }

		    return iparams;
		},

		   
		isCardinalitySatisfied : function(icard, count) {
		    if(count<0)
			return false;

		    if(icard==this.CARD_ONE)
			return count==1;

		    if(icard==this.CARD_MANY)
			return count>0;

		    return false;
		},

		transValuesOTI : function(ovalue, itype) {
		    if(!dojo.isArray(ovalue))
			return [this.transValueOTI(ovalue, itype)];

		    var ivalue=[];

		    for(var x=0; x<ovalue.length; x++)
			ivalue[x]=this.transValueOTI(ovalue[x], itype);

		    return ivalue;
		},

		transOptionsOTI : function(ooptions, itype) {
		    var ioptions=[];

		    for(var x=0; x<ooptions.length; x++)
			ioptions[x]=this.transOptionOTI(ooptions[x], itype);

		    return ioptions;
		},
		    
	        transValueOTI : function(ovalue, itype) {
		    try {
			if(itype==this.TYPE_STRING)
			    return ovalue.toString();

			if(itype==this.TYPE_INTEGER) {
			    var ovalue_num=new Number(ovalue);

			    if(ovalue_num==Number.NaN)
				return "0";

			    return (Math.floor(ovalue_num)).toString();
			}
		    }
		    catch(err) {}

		    return "";
		},

		transDefaultOTI : function(odefault, itype) {
		    return this.transValueOTI(odefault, itype);
		},

		transOptionOTI : function(ooption, itype) {
		    return this.transValueOTI(ooption, itype);
		},
		    
		transHelpOTI : function(ohelp) {
		    try {
			return ohelp.toString();
		    } catch(err) {
			return "";
		    }
		},

		transNameOTI : function(oname) {
		    try {
			return oname.toString();
		    } catch(err) {
			return "";
		    }
		},

		transGroupOTI : function(ogroup) {
		    try {
			return ogroup.toString();
		    } catch(err) {
			return "";
		    }
		},
		    
		transTypeOTI : function(otype) {
		    var otype_fixed=this._fixSpecialValue(otype);

		    if(otype_fixed=="string")
			return this.TYPE_STRING;

		    if(otype_fixed=="directory")
			return this.TYPE_STRING;

		    if(otype_fixed=="integer")
			return this.TYPE_INTEGER;

		    return this.TYPE_UNKNOWN;
		},

		transCardinalityOTI : function(ocard) {
		    var ocard_fixed=this._fixSpecialValue(ocard);
		    
		    if(ocard=="many")
			return this.CARD_MANY;

		    return this.CARD_ONE;
		},

		transRequiredOTI : function(orequired) {
		    return Boolean(orequired);
		},
		    
		transValuesITO : function(ivalues, itype) {
		    if(ivalues.length==1)
			return this.transValueITO(ivalues[0], itype);

		    var ovalues=[];

		    for(var x=0; x<ivalues.length; x++)
			ovalues[x]=this.transValueITO(ivalues[x], itype);

		    return ovalues;
		},

		transOptionsITO : function(ioptions, itype) {
		    var ooptions=[];

		    for(var x=0; x<ioptions.length; x++)
			ooptions[x]=this.transValueITO(ioptions[x], itype);

		    return ooptions;
		},

		transValueITO : function(ivalue, itype) {
		    return ivalue;
		},

		transDefaultITO : function(idefault, itype) {
		    return idefault;
		},

		transOptionITO : function(ioption, itype) {
		    return ioption;
		},

		transHelpITO : function(ihelp) {
		    return ihelp;
		},

		transNameITO : function(iname) {
		    return iname;
		},
		    
		transGroupITO : function(igroup) {
		    return igroup;
		},

		transTypeITO : function(itype) {
		    if(itype==this.TYPE_STRING)
			return "string";

		    if(itype==this.TYPE_INTEGER)
			return "integer";

		    return "";
		},

		transCardinalityITO : function(icard) {
		    if(icard==this.CARD_MANY)
			return "many";

		    return "one";
		},

		transRequiredITO : function(irequired) {
		    return irequired;
		},


		    
		transParamsOTI : function(oparams) {
		    var iparams=[];
		    var itype;
		    var obj;
		    
		    for(var x in oparams) {
			itype=this.transTypeOTI(oparams[x]["type"]);
			


			obj={
				name : this.transNameOTI(x),
				cardinality : this.transCardinalityOTI(oparams[x]["cardinality"]),
				required : this.transRequiredOTI(oparams[x]["mandatory"]),
				type : itype,
				help : this.transHelpOTI(oparams[x]["help"]),
				values : this.transValuesOTI(oparams[x]["value"], itype),
				options : this.transOptionsOTI(oparams[x]["allowed"], itype),
				group : this.transGroupOTI(oparams[x]["category"])
			};

			obj["default"]=this.transDefaultOTI(oparams[x]["default"], itype);

			iparams.push(obj);
						
			
		    }

		    iparams.sort(function(a, b) {
			    return (!a.required && b.required ? 1 : 0 );
			});

		    return iparams;
		},
		    
		transParamsITO : function(iparams) {
		    var oparams=new Object();

		    for(var x=0; x<iparams.length; x++) {
			oparams[this.transNameITO(iparams[x]["name"])]={
			    cardinality : this.transCardinalityITO(iparams[x]["cardinality"]),
			    mandatory : this.transRequiredITO(iparams[x]["required"]),
			    type : this.transTypeITO(iparams[x]["type"]),
			    help : this.transHelpITO(iparams[x]["help"]),
			    value : this.transValuesITO(iparams[x]["values"]),
			    allowed : this.transOptionsITO(iparams[x]["options"]),
			    category : this.transGroupITO(iparams[x]["group"])
			};

			oparams[this.transNameITO(iparams[x]["name"])]["default"]=this.transDefaultITO(iparams[x]["default"]);
		    }

		    return oparams;
		},
		   
		_fixSpecialValue : function(val) {
		    try {
			return dojo.string.trim(val.toString().toLowerCase());
		    } catch(err) {
			return "";
		    }
		},

		    
		TYPE_UNKNOWN : -1,
		TYPE_INTEGER : 16,
		TYPE_STRING : 32,
		CARD_ONE : 1,
                CARD_MANY : -2
		    
	    })});

