/* Phenotype Descoverer Application - Javascript 
*  written by Asher Garland
*  asher.garland@gmail.com
*/

/* Variables and lists */
var resultsVariables = new ResultsVariables();

/* Javascript run when the page is loaded */
$(document).ready(function(){

	resultsVariables.addAllVariables();
	resultsStudysCheck();
	turnOffVWhen0();

	restoreFilterDefaults();
	applyDisplayOptions();

	/* Key press listener */
	$('#advanced-search-container').keyup(function(event){
		buildAdvancedSearchBuffer();
	});
	$('.advanced-search-option-box').keyup(function(event){
		buildAdvancedSearchBuffer();
	});

	/* Add Mouse click event listeners */
	$('select.advanced-search-tag').change(function(event){
		buildAdvancedSearchBuffer();
	});
	$('select.advanced-search-option').change(function(event){
		buildAdvancedSearchBuffer();
	});

	$('#results_table tbody tr input').change(function(event){
   		toggleSelected(this.id);
   }); 

	$('#variables_table tbody tr input').change(function(event){
   		toggleSelected(this.id);
   }); 

	$('#limit-button').click(function(event){
   		toggleLimits();
   });

	$('#limit-reset-button').click(function(event){
   		toggleLimits();
   });

	$('#login-button').click(function(event){
   		checkLoginForm();
   	});

	$('#createLogin-button').click(function(event){
   		checkNewUserForm();
   	});
	
	$('#newUser-button').click(function(event){
   		toggleCreateLogin();
   });

	$('#cancel-newUser-button').click(function(event){
   		toggleCreateLogin();
   });

   $('#resultsCheckButton').click(function(event){
		resultsCheckAll();
   });

   $('#filter_defaults').click(function(event){
   		restoreFilterDefaults();
   		applyDisplayOptions();
   });

   $('input#studyType').click(function(event){
   		toggleStudyTypeFilters();
   });

   $('#search-bar-add').click(function(event){
   		addAdvancedSearchBar();
   });
   
   $('#clearAdvancedSearch').click(function(event){
   		removeAllAdvancedSearchBars();
   		clearAllAdvancedOptions();
   });

   $('#tabs li').click(function(event){
   		changeTabTarget(this.id);
   		//update checkall uncheck all button text
	   	var $button = $('#resultsCheckButton');
	   	if ( resultsIsSelected() )
	   	{
	   		$button.html('Uncheck All');
	   		$('#resultsDisplayButton').html('Display');
	   	}
	   	else
	   	{
	   		$button.html('Check All');
	   		$('#resultsDisplayButton').html('Display All');
	   	}

   });

   $('.advanced-search-option-selectable').click(function(event){
   		optionSelected(this.id);
   });

   $('#filter_apply').click(function(event){
   		applyDisplayOptions();
   		/* Feb 8th, quick fix */
   		$(".wrapper1").scroll(function(){
		    $(".wrapper2").scrollLeft($(".wrapper1").scrollLeft());
		});
		$(".wrapper2").scroll(function(){
		    $(".wrapper1").scrollLeft($(".wrapper2").scrollLeft());
		});
        /* Feb 8th end */
	});

   $('#saveAdvancedSearch').click(function(event){
   		advancedHistorySave( $('#searchBuffer').val() );
   })

   $('.historyAddAND').click(function(event){
   		advancedHistoryAdd(this, true);
   });

   $('.historyAddOR').click(function(event){
   		advancedHistoryAdd(this, false);
   });

	$('#pageJumpMenu').change(function(event){
		pageJump();
	});

	$('button.pageJumpTop').click(function(event){
		window.location.hash = 'top';
		window.location.hash = '';
	});

	$('input.advanced-list').change(function(event){
		selectAdvancedOption(this);
		buildAdvancedSearchBuffer();	
	});
	
	/*
	$('.advanced-search-option-selectable').click(function(event){
		$(this).toggleClass('highlighted');
	});
	*/

	$('#resultsDisplayButton').click(function(event){
		displaySelected();
	});

	$('.hierarchyParentImg').click(function(event){
		event.stopPropagation();
		toggleDisplayChildren($(this).parent().get(0));
	});

	/* UI Update February 6th Start */
	$(".wrapper1").scroll(function(){
		    $(".wrapper2").scrollLeft($(".wrapper1").scrollLeft());
	});
	$(".wrapper2").scroll(function(){
	    $(".wrapper1").scrollLeft($(".wrapper2").scrollLeft());
	});   
	/* UI Update February 6th End */

   /* jQuery tooltip */
   /* Results Table Mouse over Pop Up */
	var $resultsTooltip = $('#tooltip'), // reusable jQuery obj
    resultOffset = {x: 20, y: 0}; // tooltip offset from the cursor'
    var pageHeight;
	$('#results_table td.title').mouseover(function(event) {
	    pageHeight = $(document).height();
	    console.log(pageHeight);
	    //display tooltip
	    $resultsTooltip.show();
	}).mousemove(function(e) { // move
	    // set the positioning with offset
	    console.log((e.pageY + $resultsTooltip.height() + resultOffset.y));
	    if ( (e.pageY + $resultsTooltip.height() + resultOffset.y) > pageHeight )
	    {
	    	var newY = e.pageY - ((e.pageY + $resultsTooltip.height() + resultOffset.y) - pageHeight);
	    	$resultsTooltip.css({left: e.pageX + resultOffset.x, top: newY});
	    }
	    else
	    {
			$resultsTooltip.css({left: e.pageX + resultOffset.x, top: e.pageY + resultOffset.y}) 
	    }
	    // set the tooltip HTML contents
	    $resultsTooltip.html(
	    	fillTooltipBody($(this).closest('tr').attr('id'))
	    );
	}).mouseout(function() {
	    //hide
	    $resultsTooltip.hide();
	});

	/* Variables Tab Table Mouse over Pop up */
	var $variableTooltip = $('#tooltip'), // reusable jQuery obj
    variableOffset = {x: 20, y: -100}; // tooltip offset from the cursor'
	$('div.var_name').mouseover(function(event) {
	    pageHeight = $(document).height();
	    //display tooltip
	    $variableTooltip.show();
	}).mousemove(function(e) { // move
	    // set the positioning with offset
	    if ( (e.pageY + $variableTooltip.height() + variableOffset.y) > pageHeight )
	    {
	    	var newY = e.pageY - ((e.pageY + $variableTooltip.height() + variableOffset.y) - pageHeight);
	    	$variableTooltip.css({left: e.pageX + variableOffset.x, top: newY});
	    }
	    else
	    {
			$variableTooltip.css({left: e.pageX + variableOffset.x, top: e.pageY + variableOffset.y}) 
	    }
	    // set the tooltip HTML contents
    	var rowId = $(this).parent().parent().attr('id');
	    $variableTooltip.html(
	    	fillVariableToolTip( rowId )
	    );
	}).mouseout(function() {
	    //hide
	    $variableTooltip.stop(true).hide();
	});

	/* Mother/Daughter node tool tip*/
	/* Create a hidden tooltip div in the webpage. */
	var $nodeTooltip = $("#nodeToolTip");
	var nodeOffset = {x: 20, y: -100}; // tooltip offset from the cursor
	$('.mother').click(function(event) {
		event.stopPropagation();
		event.preventDefault();
		pageHeight = $(document).height();
		//check for old selected node 
		$old = $('.mother.selected').add('.daughter.selected');
		if ( $old.length != 0 )
		{
			$old = $($old.get(0));
			$old.removeClass('selected');
			//hide
			$nodeTooltip.stop(true).hide();
		}
		if ( !$(this).hasClass('selected') && !$old.is($(this)) )
		{
			//add class selected
			$(this).addClass('selected');
		    //display tooltip
		    $nodeTooltip.stop(true).show();
		    // set the tooltip HTML contents
		    $nodeTooltip.html(
		    	fillMotherTooltipBody($(this).closest('tr').attr('id'))
		    );
		    // set the positioning with offset
		    if ( (event.pageY + $nodeTooltip.height() + nodeOffset.y) > pageHeight )
		    {
		    	var difference = (event.pageY + $nodeTooltip.height() + nodeOffset.y) - pageHeight;
		    	var newY = event.pageY - difference;
		    	$nodeTooltip.css({left: event.pageX + nodeOffset.x, top: newY});
		    }
		    else
		    {
				$nodeTooltip.css({left: event.pageX + nodeOffset.x, top: event.pageY + nodeOffset.y});
		    }
		}
	});
	$('.daughter').click(function(event) {
		event.stopPropagation();
		event.preventDefault();
		pageHeight = $(document).height();
		//check for old selected node 
		$old = $('.daughter.selected').add('.mother.selected');
		if ( $old.length != 0 )
		{
			$old = $($old.get(0));
			$old.removeClass('selected');
			//hide
			$nodeTooltip.stop(true).hide();
		}
		if ( !$(this).hasClass('selected') && !$old.is($(this)) )
		{
			//add class selected
			$(this).addClass('selected');
		    //display tooltip
		    $nodeTooltip.stop(true).show();
		    // set the tooltip HTML contents
		    $nodeTooltip.html(
		    	fillDaughterTooltipBody($(this).closest('tr').attr('id'))
		    );
		    // set the positioning with offset
		    if ( (event.pageY + $nodeTooltip.height() + nodeOffset.y) > pageHeight )
		    {
		    	var difference = (event.pageY + $nodeTooltip.height() + nodeOffset.y) - pageHeight;
		    	var newY = event.pageY - difference;
		    	$nodeTooltip.css({left: event.pageX + nodeOffset.x, top: newY});
		    }
		    else
		    {
				$nodeTooltip.css({left: event.pageX + nodeOffset.x, top: event.pageY + nodeOffset.y});
		    }
		}
	});

	var $displayOptionsHelpToolTip = $('div#display-options-help-tooltip'), // reusable jQuery obj
    /* Display option Pop-up Help Tooltips */
    displayOffset = {x: 10, y: -100}; // tooltip offset from the cursor
	$('#filters td').mouseover(function(event) {
		    //display tooltip
		    $displayOptionsHelpToolTip.stop(true).show();
	}).mousemove(function(e) { // move
	    // set the positioning with offset
	    $displayOptionsHelpToolTip.css({left: e.pageX + displayOffset.x, top: e.pageY + displayOffset.y}) 
	    // set the tooltip HTML contents
		var $childId = $(this).children("input").attr('id');
	    $displayOptionsHelpToolTip.html(
	    	filldisplayOptionsHelpToolTipBody($childId)
	    );
	}).mouseout(function() {
	    //hide
	    $displayOptionsHelpToolTip.stop(true).hide();
	});

	/* VDAS icon Pop-up Tooltips */
	displayOffset = {x: 10, y: 0}; // tooltip offset from the cursor
	$('.detailsImg').mouseover(function(event) {
			event.stopPropagation();
			event.preventDefault();
		    //display tooltip
		    $displayOptionsHelpToolTip.stop(true).show();
	}).mousemove(function(e) { // move
	    // set the positioning with offset
	    $displayOptionsHelpToolTip.css({left: e.pageX + displayOffset.x, top: e.pageY + displayOffset.y}) 
	    // set the tooltip HTML contents
	    $displayOptionsHelpToolTip.html(
	    	displayVDASCount(this)
	    );
	}).mouseout(function() {
	    //hide
	    $displayOptionsHelpToolTip.stop(true).hide();
	});

	var $helpToolTip = $('#help-tooltip'); // reusable jQuery obj
    var xcord;
    var ycord;
    /* Search Bar Help icon Tooltip */
	$('img#search-bar-help').mouseover(function() {
		    //display tooltipxcord =  $('img#advanced-options-help').position().left - 500; 
		    xcord =  $('img#search-bar-help').position().left - 450;
		    ycord =  $('img#search-bar-help').position().top - 45;
		    $helpToolTip.stop(true).show();
	}).mousemove(function(e) { // move
	    // set the positioning with offset
	    $helpToolTip.css({left: xcord, top: ycord}) 
	    // set the tooltip HTML contents
	    $helpToolTip.html(
	    	fillHelpTooltip(this.id)
	    );
	}).mouseout(function() {
	    //hide
	    $helpToolTip.stop(true).hide();
	});
	/* Advanced Options Help icon Tooltip */
	$('img#advanced-options-help').mouseover(function() {
		    //display tooltip
		    xcord =  $('img#advanced-options-help').position().left - 450; 
		    ycord =  $('img#advanced-options-help').position().top - 80;
		    $helpToolTip.stop(true).show();
	}).mousemove(function(e) { // move
	    // set the positioning with offset
	    if ( (ycord + $helpToolTip.height()) > pageHeight )
	    {
	    	var difference = (ycord + $helpToolTip.height()) - pageHeight;
		    var newY = ycord - difference;
	    	$helpToolTip.css({left: xcord, top: newY});
	    }
	    else
	    {
	    	$helpToolTip.css({left: xcord, top: ycord}) 
	    }
	    // set the tooltip HTML contents
	    $helpToolTip.html(
	    	fillHelpTooltip(this.id)
	    );
	}).mouseout(function() {
	    //hide
	    $helpToolTip.stop(true).hide();
	});
	/* Display Options Help icon Tooltip */
	$('img#display-options-help').mouseover(function() {
		    //display tooltip
		    xcord =  $('img#display-options-help').position().left - 450; 
		    ycord =  $('img#display-options-help').position().top - 35;
		    $helpToolTip.stop(true).show();
	}).mousemove(function(e) { // move
	    // set the positioning with offset
	    $helpToolTip.css({left: xcord, top: ycord}) 
	    // set the tooltip HTML contents
	    $helpToolTip.html(
	    	fillHelpTooltip(this.id)
	    );
	}).mouseout(function() {
	    //hide
	    $helpToolTip.stop(true).hide();
	});

		var BrowserDetect = {
		init: function () {
			this.browser = this.searchString(this.dataBrowser) || "An unknown browser";
			this.version = this.searchVersion(navigator.userAgent)
				|| this.searchVersion(navigator.appVersion)
				|| "an unknown version";
			this.OS = this.searchString(this.dataOS) || "an unknown OS";
		},
		searchString: function (data) {
			for (var i=0;i<data.length;i++)	{
				var dataString = data[i].string;
				var dataProp = data[i].prop;
				this.versionSearchString = data[i].versionSearch || data[i].identity;
				if (dataString) {
					if (dataString.indexOf(data[i].subString) != -1)
						return data[i].identity;
				}
				else if (dataProp)
					return data[i].identity;
			}
		},
		searchVersion: function (dataString) {
			var index = dataString.indexOf(this.versionSearchString);
			if (index == -1) return;
			return parseFloat(dataString.substring(index+this.versionSearchString.length+1));
		},
		dataBrowser: [
			{
				string: navigator.userAgent,
				subString: "Chrome",
				identity: "Chrome"
			},
			{ 	string: navigator.userAgent,
				subString: "OmniWeb",
				versionSearch: "OmniWeb/",
				identity: "OmniWeb"
			},
			{
				string: navigator.vendor,
				subString: "Apple",
				identity: "Safari",
				versionSearch: "Version"
			},
			{
				prop: window.opera,
				identity: "Opera",
				versionSearch: "Version"
			},
			{
				string: navigator.vendor,
				subString: "iCab",
				identity: "iCab"
			},
			{
				string: navigator.vendor,
				subString: "KDE",
				identity: "Konqueror"
			},
			{
				string: navigator.userAgent,
				subString: "Firefox",
				identity: "Firefox"
			},
			{
				string: navigator.vendor,
				subString: "Camino",
				identity: "Camino"
			},
			{		// for newer Netscapes (6+)
				string: navigator.userAgent,
				subString: "Netscape",
				identity: "Netscape"
			},
			{
				string: navigator.userAgent,
				subString: "MSIE",
				identity: "Explorer",
				versionSearch: "MSIE"
			},
			{
				string: navigator.userAgent,
				subString: "Gecko",
				identity: "Mozilla",
				versionSearch: "rv"
			},
			{ 		// for older Netscapes (4-)
				string: navigator.userAgent,
				subString: "Mozilla",
				identity: "Netscape",
				versionSearch: "Mozilla"
			}
		],
		dataOS : [
			{
				string: navigator.platform,
				subString: "Win",
				identity: "Windows"
			},
			{
				string: navigator.platform,
				subString: "Mac",
				identity: "Mac"
			},
			{
				   string: navigator.userAgent,
				   subString: "iPhone",
				   identity: "iPhone/iPod"
		    },
			{
				string: navigator.platform,
				subString: "Linux",
				identity: "Linux"
			}
		]

	};
	BrowserDetect.init();
	detectBrowserCompatibilityIssue(BrowserDetect);
});


/* Table Row Selection detection */
function isSelected (id) {
	var string = '#' + id; 
	if ( $(string).hasClass('selected') )
	{
		return true;
	} 
	return false;
}

/* Table Row Selection */
function toggleSelected (id) {
	//add or remove selected class to table row
	var string = '#' + id;
	var $checkbox = $(string + ' input');
   	if ( isSelected(id) )
   	{
   		$(string).removeClass('selected');
   		$checkbox.attr('checked', false);
   	}
   	else
   	{
   		$(string).addClass('selected');
   		$checkbox.attr('checked', true);
   	}

   	//update checkall uncheck all button text
   	var $button = $('#resultsCheckButton');
   	if ( resultsIsSelected() )
   	{
   		$button.html('Uncheck All');
   		$('#resultsDisplayButton').html('Display');
   	}
   	else
   	{
   		$button.html('Check All');
   		$('#resultsDisplayButton').html('Display All');
   	}
}

/* Advanced search option, is selected? */
function optionIsSelected (id)
{
	var string = '#' + id; 
	if ( $(string).hasClass('advanced-search-option-selected') )
	{
		return true;
	} 
	return false;
}

/* Advanced Search page Option selected */
function optionSelected (id)
{
	var selected = '#' + id;

   	if ( optionIsSelected(id) )
   	{
   		$(selected).removeClass('advanced-search-option-selected');
   		$(selected).addClass('advanced-search-option-selectable');
   	}
   	else
   	{
   		$(selected).removeClass('advanced-search-option-selectable');
   		$(selected).addClass('advanced-search-option-selected');
   		/* expand to the parent, see if any options are selected, if they are deselect them and select the new one -- functionality not desired
   		var parentContainer = $(selected).parent();
   		var previouslySelected = parentContainer.children('.advanced-search-option-selected')
   		if ( previouslySelected.length )
   		{
   			$('#' + previouslySelected[0].id).removeClass('advanced-search-option-selected');
   			$('#' + previouslySelected[0].id).addClass('advanced-search-option-selectable');
   		}
   		$(selected).addClass('advanced-search-option-selected');
   		*/
   	}
}

/* Select all Table Rows on Results Page */
function resultsCheckAll () {
	var targetId = $('.target').attr('id');
	var $rows = $('#'+targetId + ' table tbody').find('tr');
	var $button = $('#resultsCheckButton');
	//check to see if any rows are selected
	if ( resultsIsSelected() )
	{
		//unselect all
		$rows.each(function(index) {
			if ( this.id != "" && isSelected(this.id))
			{
				toggleSelected(this.id);
			}		
		});	
		$button.html('Check All');
	}
	else
	{
		//select all
		$rows.each(function(index) {
			if ( this.id != "" && !isSelected(this.id) && !$(this).hasClass('hide') )
			{
				toggleSelected(this.id);
			}		
		});	
		$button.html('Uncheck All');
	}
}

/* Check if ANY Table Rows of Results table are selected */
function resultsIsSelected () {
	var flag = 0;
	var targetId = $('.target').attr('id');
	var $rows = $('#'+targetId + ' table tbody').find('tr');
	$rows.each(function(index) {
    	if( isSelected(this.id) )
    	{
    		flag = 1;
    	}
	});
	return flag;
}

/* Results page Meta Data options - set to default */
function restoreFilterDefaults () {
	var $filters = $('#filters td input');
	$filters.each(function(index) {
		//set all to unchecked besides the defaults
		switch ( this.id )
		{
			case 'title':
			case 'embargoRelease':
			case 'details':
			case 'platform':
			case 'sampleSize':
			case 'studyType': 	
			case 'studyDesign':
			case 'sampleType':
			case 'sampleRole':
			case 'other':
								this.checked = true;
								break;
			default:
								this.checked = false;
								break; 
		}
	});
	toggleStudyTypeFilters();
}

function toggleStudyTypeFilters () {
	var $typeCheckbox = $('input#studyType');
	var $filters = $('#filters td input');

	var isChecked = $typeCheckbox.attr('checked');
	$filters.each(function(index) {
		//set all to unchecked besides the defaults
		switch ( this.id )
		{ 
			case 'studyDesign':
			case 'sampleType':
			case 'sampleRole':
			case 'other':
								this.checked = isChecked;
								this.disabled = !(isChecked);
								break;
		}
	});
}

/* Fills the body of the tooltip on the results page with the corresponding title and text information */
function fillTooltipBody(id) {
	var string = '#' + id;
	var $title = $(string).find('.title').text();
	var title = "<h1 class='tooltip'>" + $title + "</h1>";
	var body = "<p class='tooltip'>"+ $('#'+id).find('.highlight1').text() +"</p>";
	var content = title + body;
	return content;
}

/* Varibale Results Tab Tool Tip Text Fill on Mouse Over */
function fillVariableToolTip( rowId ) {
	var variable = resultsVariables.getVariableResult( new String(rowId) );
	var content = new String("");
	content += '<h1 class="nomargin justify-center">'+variable.var_name+'</h1>';
	content += "<table class='recentlyAdded'>"+
				"<tr><td><p>Study:</p></td><td>"+variable.study+"</td></tr>"+
				"<tr><td><p>Description:</p></td><td>"+variable.description+"</td></tr>"+
				"<tr><td><p>Dataset:</p></td><td>"+variable.dataset+"</td></tr>"+
				"<tr><td><p>Data Type:</p></td><td>"+variable.datatype+"</td></tr>"+
				"<tr><td><p>Unit of Measurement:</p></td><td>"+variable.units+"</td></tr>"+
				"<tr><td><p>Max:</p></td><td>"+variable.max+"</td></tr>"+
				"<tr><td><p>Min:</p></td><td>"+variable.min+"</td></tr></table>";
	return content;
}

function filldisplayOptionsHelpToolTipBody(id)
{
	var string = "<p class='help-tooltip'>";

	switch (id)
	{
		case 'studyType': 		string += 'Study Type: Information about the type of Study conducted';break;
		case 'title': 			string += 'Title: Information about Study Name and ID'; break;
		case 'links': 			string += 'Links: Additional information'; break;
		case 'studyDesign': 	string += 'Study Design: The formulation of trials and experiments in medical and epidemiological research'; break;
		case 'details': 		string += 'Details: Contains options to view study Variables, Datasets, Analyses, and Study Documents'; break;
		case 'geography': 		string += 'Geography: Geographical location of the study'; break;
		case 'sampleType': 		string += 'Sample Type: Whether the sample is Representative or Non-representative'; break;
		case 'embargoRelease': 	string += 'Embargo Release: The expiration date of publication exclusivity rights given to contributing investigators'; break;
		case 'irb': 			string += 'IRB: Whether Institutional Review Board is required or not'; break;
		case 'sampleRole': 		string += 'Sample Role: Whether the sample is Case or Control'; break;
		case 'platform': 		string += 'Platform: Type of sequencing platform used'; break;
		case 'consentType': 	string += 'Consent Type: Data use constraint'; break;
		case 'sampleSize': 		string += 'Sample Size: Number of participants<br/>by gender<br/>by race<br/>by ethnicity<br/>by age group<br/>by sample role'; break;
		case 'topicDisease': 	string += 'Topic Disease: Health topic of the study'; break;
		case 'other': 			string += 'Other: Information about form of treatment and level of detail of observations made'; break;
	}
	string += '</p>';
	return string;
}

function fillHelpTooltip (id)
{
	var string = "<p class='help-tooltip'>";

	switch (id)
	{
		case 'search-bar-help': string += '<b>Syntax:</b><br>- Use quotation marks when you want to search two words as one term. E.g. &quot;Heart attack&quot;<br>- Connect multiple terms by Boolean operators (AND, OR). E.g. asthma OR &quot;chronic obstructive pulmonary disease&quot;<br>&quot;Heart attack&quot; AND BMI<br>&quot;Heart attack&quot; AND (BMI OR weight)<br><br><b>Type of search:</b><br>- The default search type is &quot;concept-based&quot;. This expands your search using synonymous or more specific terms.<br>- For example, when you search &quot;heart attack&quot; using the concept-based option, PhenDisco searches other synonymous terms such as &quot;heart attack&quot; and &quot;myocardial infarction&quot;.<br>- If you want to retrieve the studies that have your search term in its exact form in the database, unclick the &quot;concept-based&quot; box on the right side of the search bar.<br><br><b>Limits:</b></br>- You can limit your search by clicking on the Limits button below the search bar. This opens a box for Limits options.</br>- You can limit your search to the following fields by using the drop down menu: Topic Disease, Study Description, Study ID, Study Name, Variable Description, Variable ID, Variable Name, Attribution.</br>- Once limit is selected, click the search button.</br>- For example, if you wanted to search for a specific study, e.g. NHLBI GO ESP: Early-Onset Myocardial Infarction, type the name of the study into the search box and limit your search to &quot;Study Name&quot;.</br>- When searching by Study ID, use the main ID without the version suffix.</br>E.g. phs000494.v1.p1 should be searched as &quot;phs000494&quot;.'; break;
		case 'advanced-options-help': string += 'Use advanced search to build a query by specifying search fields. Additional search terms can be included by clicking the + icon. The once built, the query is run by clicking Submit Query. Use Clear All to start the search over. The query builder is combined representation of the search parameters that allows editing.'; break;
		case 'display-options-help': string += '<b>Display Options:</b><br>- Check data fields to be shown. The Apply button will update the result table with the selected fields.<br>- To restore the default view, Click Restore Defaults.<br>- Move the mouse over the question mark on the right side of the page to get these directions.<br>- Move the mouse over each option to view a description.<br><br><b>Basic Results:</b><br>- Above the table you will see how many studies are being displayed out of the total studies found.<br>- There are arrows to view each page of the results.<br>- Scroll horizontally at the top or bottom of the display table to view additional columns.<br>- The Details column contains four boxes. Mouse over the colored boxes to display content information.<br></br><b>Search Relevancy:</b></br>- Scroll over a study, the row is highlighted in yellow and the Study Name and ID will appear in the popup box.</b>- The search terms will be highlighted in yellow where it shows up in Study Names and descriptions.</b>- Each study has a relevancy ranking out of five stars. A five star ranking corresponds to a very relevant result, while a one star ranking is a slightly relevant result.</br></br><b>Viewing Studies:</b></b>- Click on the Study Name and ID in the Title box for the study to open in a new page.</br></br><b>Exporting Results:</b></br>- There are three buttons on top of the display table: &quot;Display All&quot;, &quot;Check All&quot;, and &quot;ExportSelections&quot;. The &quot;Check All&quot; button will select each of the studies present on that page. The&quot;Export Selections&quot; will export a list of Study ID, Study Name, Type of Study, Participants, and Datasets of the checked studies in the comma separated value (CSV) format.';break;
	}
	string += '</p>'; 
	return string;
}

function displayVDASCount (icon)
{
	var $vdas = $(icon);
	var flag = $(icon).hasClass('on');
	var string = "<p class='help-tooltip'>";
	var selected;

	if  ( $vdas.hasClass('v') )
	{
		/* V image selected */
		selected = 'v';
	}
	else if ( $vdas.hasClass('d') )
	{
		/* D image selected */
		selected = 'd';
	}
	else if ( $vdas.hasClass('a') )
	{
		/* A image selected */
		selected = 'a';
	}
	else 
	{
		/* S image selected */
		selected = 's';
	}

	if ( flag )
	{
		switch (selected)
		{
			case 'v': 	/* V*/
						var phenNum = $vdas.parent().parent().find('.PhenNum').text();
						string += "Study has " + phenNum + " Variable components"
						/* Function to append number of Variables*/
						break;
			case 'd': 	/* D */
						string += "Study has Document components"
						/* Function to append number of Documents*/
						break;
			case 'a': 	/* A */
						string += "Study has Analyses components"
						/* Function to append number of Analyses*/
						break;
			case 's': 	/* S */
						string += "Study has SRA components"
						break;
		}
	}
	else
	{
		switch (selected)
		{
			case 'v': 	/* V*/
						string += "Study has no Variable components"
						/* Function to append number of Variables*/
						break;
			case 'd': 	/* D */
						string += "Study has no Document components"
						/* Function to append number of Documents*/
						break;
			case 'a': 	/* A */
						string += "Study has no Analyses components"
						/* Function to append number of Analyses*/
						break;
			case 's': 	/* S */
						string += "Study has no SRA components"
						break;
		}
	}

	string = string + '</p>'; 
	return string;
}


/* Adds an additional search bar to the advanced search page */
function addAdvancedSearchBar () {
	var $container = $("#secondary-search-container");
	var $searchBars = $('div.advanced-search-bar');
	var count = 0;
	//count the number of search bars
	count = $searchBars.length;
	//append search bar to the end
	if (count < 5)
	{
		$container.append("<div class='container advanced-search-bar' id='searchBar_"+ count +"'><!-- Drop down menu --><div class='container alignleft'><select class='advanced-search-option' id='searchBar_"+ count +"'><option value='AND'>And</option><option value='OR'>Or</option></select></div><!-- Drop down menu --><div class='container alignleft'><select class='advanced-search-tag' id='searchBar_"+ count +"'><option selected='selected' value='All Fields'>All Fields</option><option value='Analysis'>Analysis</option><option value='Analysis ID'>Analysis ID</option><option value='Analysis Name'>Analysis Name</option><option value='Ancestor'>Ancestor</option><option value='Attribution'>Attribution</option><option value='Belongs To'>Belongs To</option><option value='Dataset'>Dataset</option><option value='Dataset ID'>Dataset ID</option><option value='Dataset Name'>Dataset Name</option><option value='Discriminator'>Discriminator</option><option value='Disease'>Disease</option><option value='Document'>Document</option><option value='Document ID'>Document ID</option><option value='Document Name'>Document Name</option><option value='Document Part'>Document Part</option><option value='Filter'>Filter</option><option value='Genotype Platform'>Genotype Platform</option><option value='Has Analysis'>Has Analysis</option><option value='Has Dataset'>Has Dataset</option><option value='Has Document'>Has Document</option><option value='Has PhenX Mapping'>Has PhenX Mapping</option><option value='Has Variable'>Has Variable</option><option value='Is Root Study'>Is Root Study</option><option value='Is Top-Level Study'>Is Top-Level Study</option><option value='Object Type'>Object Type</option><option value='PhenX'>PhenX</option><option value='Project'>Project</option><option value='Study'>Study</option><option value='Study Archive'>Study Archive</option><option value='Study Has SRA Components'>Study Has SRA Components</option><option value='Study ID'>Study ID</option><option value='Study Name'>Study Name</option><option value='Variable'>Variable</option><option value='Variable Description'>Variable Description</option><option value='Variable ID'>Variable ID</option><option value='Variable Name'>Variable Name</option></select></div><!-- Search Bar --><div class='container alignleft'><input class='advanced-search-bar' type='text' name='query' id='searchBar_"+ count +"' value=''> </div><!-- Plus and Minus icons --><div class='container alignleft'><img onclick='removeAdvancedSearchBar(this)' class='search-bar-remove' id='searchBar_" + count + "' src='./images/minus.png' alt='Add Search Option' height='16' width='16'></div><!-- Result Count <div class='container alignleft'><span id='search_result_"+ count +"'>Items Found: 0</span></div>--><div style='clear: both;'></div></div>");
		/* Add Mouse click event listeners */
		$('select.advanced-search-tag').change(function(event){
			buildAdvancedSearchBuffer();
		});
		$('select.advanced-search-option').change(function(event){
			buildAdvancedSearchBuffer();
		});
	}

}

/* Removes all additional search bars to the advanced search page */
function removeAllAdvancedSearchBars () {
	//remove all the search bars
	$("#secondary-search-container").empty();
	$("#primary-advanced-search-container input.advanced-search-bar").val('');
	// reset search buffer
	buildAdvancedSearchBuffer();
}

function clearAllAdvancedOptions () {
	$selected = $('.advanced-search-option-selected');
	$selected.removeClass('advanced-search-option-selected');
	$selected.addClass('advanced-search-option-selectable');
}

/* Removes a selected search bar from the advanced search page */
function removeAdvancedSearchBar (e) {
	// remove target search bar
	e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);	
	// rebuild search buffer
	buildAdvancedSearchBuffer ();
}

/* Builds the search query from all the advanced search bars on the advanced search page */
function buildAdvancedSearchBuffer () {
	var $searchBars = $('input.advanced-search-bar');
	var $buffer = $('#searchBuffer');
	var string = "";

	//Build the search buffer string
	$searchBars.each(function(index){
		var option = $('#' + this.id + ' select.advanced-search-option option:selected');
		var tag = $('#' + this.id + '.advanced-search-tag option:selected'); 
		//Remove Bad White Space
		this.value = this.value.replace(/\s+/g, ' ');
		//Add the option (i.e. AND|OR)
		if ( option.length && this.value != "" && this.value != " " && string != "" && string != " " )
		{
			string += " " + option[0].value + " ";
		}
		//Add the string
		string += this.value; 
		//Add the tag (i.e. [Study Name])
		if ( this.value != "" && this.value != " " && string != "" && string != " " )
		{
			string += '[' + tag.text() + ']';
		}
	});
	//Add the Advanced Options
	if ( string != "" )
	{
		string += " AND ";
	}
	string += getAdvancedOptionsBufferStrings ();
	//Check if string is empty
	if ( string == "" || string == " " )
	{
		string = "Use the builder above to create your search";
	}
	// Update the Buffer string value to be displayed
	$buffer.val(string);
}

function changeTabTarget(id)
{
	$newTarget = $('li#' + id);
	$oldTarget = $('li.target');

	if ( $newTarget.hasClass('target') == false )
	{
		//remove class target from previous target
		if ( $oldTarget.hasClass('target') )
		{
			//remove target class from old tab
			$oldTarget.removeClass('target');
			//hide the old target div
			var oldId = $oldTarget.attr('id');
			$('div#'+oldId).addClass('hide');
			
		}
		//add class target to new target
		$newTarget.addClass('target');
		//display new target div
		var newId = $newTarget.attr('id');
		$('div#'+newId).removeClass('hide');
	}

}

function toggleLimits() 
{
	$container = $('#limit-container');
	if ($container.hasClass('hide'))
	{
		$container.stop(true, true).slideDown('fast');
		$container.toggleClass('hide');
	}
	else
	{
		$container.stop(true, true).slideUp('fast');
		$container.toggleClass('hide');
	}
	
}

function displayOption (id , option)
{
	var $rows = $('#results_table');
	$rows.each(function() {
		var $row = $(this);
		var $element = $row.find('.' + id);
		if ( option == true )
		{
			$element.removeClass('hide');
		}
		else
		{
			$element.addClass('hide');
		}
	});
}

function applyDisplayOptions ()
{
	var $filters = $('table#filters').find('input');
	$filters.each(function () {
		var $option = $(this);
		if ( $option.is(':checked') )
		{
			displayOption( $option.attr('id'), true );
		}
		else
		{
			displayOption( $option.attr('id'), false );
		}
	});

		$('.div1').width($('#results_table').width());
}

/* Input: rowId(String) is the id of the result in the table of results
			rank(int) [0,5] rank, 5 is highest/most relavent. 
	error: if incorrect rank integer passed rank is default set to 0
 */
function setResultRating (rowId, rating )
{
	$stars = $('#'+rowId).find('.rating').children('div');
	switch (rating)
	{
		case 5: $stars.removeClass();
				$stars.addClass('rank5');
				break;
		case 4: $stars.removeClass();
				$stars.addClass('rank4');
				break;
		case 3: $stars.removeClass();
				$stars.addClass('rank3');
				break;
		case 2: $stars.removeClass();
				$stars.addClass('rank2');
				break;
		case 1: $stars.removeClass();
				$stars.addClass('rank1');
				break;
		case 0: 
		default: $stars.removeClass();
				$stars.addClass('rank0');
				break;

	}
}

function advancedHistorySave( searchText ) {
	if ( searchText == "Use the builder above to create your search" )
	{
		return;
	}

	var $table = $('#advanced-history');
	var $lastRow = $('#advanced-history tr:last');
	var $rows = $($table).find('tbody').find('tr');

	//determine the row number
	var count = 0;
	for ( var i = 0; i < $rows.size(); i++ ){
		count++;
	}

	var newDate = new Date();
	var dateString = (newDate.getMonth() + 1) + "-" + newDate.getDate() + "-" + newDate.getFullYear() 
					+ " " + newDate.getHours() + ":" + newDate.getMinutes() + ":" + newDate.getSeconds();

	//Append new row to the end
	$lastRow.after('<tr>'
		+ '<td class="index">' + count + '</td><td class="study">' + searchText 
		+ '</td><td class="results"></td><td class="time">' + dateString + '</td>'
		+ '<td class="add">'
		+ '<button class="historyAddAND" type="button" >And</button> '
		+ '<button class="historyAddOR" type="button" >Or</button></td>'
		+ '</tr>');

}

function advancedHistoryAdd( button, boolean ) {
	var $buffer = $('#searchBuffer');
	var $row = $(button).parent().parent();
	var study = $row.find('.study').html();
	var id = $row.attr('id');
	var string = $buffer.val();

	if ( string == "Use the builder above to create your search" )
	{
		string = "";
	}
	else
	{
		string += " ";
		if ( boolean )
		{
			string += 'AND ';
		}
		else
		{
			string += 'OR '
		}
	}
	string += study;

	$buffer.val(string);
}

function pageJump() {
	var selected = $('#pageJumpMenu option:selected');
	switch (selected.val())
	{
		case "submissionPolicy": window.location.hash = "submissionPolicy";break;
		case "dataContent": window.location.hash = "dataContent";break;
		case "accessData":  window.location.hash = "accessData";break;
		case "submitting":  window.location.hash = "submitting";break;
		case "glossary":  window.location.hash = "glossary";break;

		case "studyPage_studyDescription": window.location.hash = "studyPage_studyDescription";break;
		case "studyPage_authorizedAccess": window.location.hash = "studyPage_authorizedAccess";break;
		case "studyPage_publicData":  window.location.hash = "studyPage_publicData";break;
		case "studyPage_criteria":  window.location.hash = "studyPage_criteria";break;
		case "studyPage_molecularData":  window.location.hash = "studyPage_molecularData";break;
		case "studyPage_studyHistory":  window.location.hash = "studyPage_studyHistory";break;
		case "studyPage_publications":  window.location.hash = "studyPage_publications";break;
		case "studyPage_relatedDiseases":  window.location.hash = "studyPage_relatedDiseases";break;
		case "studyPage_links":  window.location.hash = "studyPage_links";break;
		case "studyPage_requests":  window.location.hash = "studyPage_requests";break;
		case "studyPage_studyAttribution":  window.location.hash = "studyPage_studyAttribution";break;
	}
}

function onVDASClick (element) {
	var $vdas = $(element);
	var $rows = $('#results_table tr');
	var selected;

	/* Check if v, d, a, or s */
	if  ( $vdas.hasClass('v') )
	{
		/* V image selected */
		selected = 'v';
	}
	else if ( $vdas.hasClass('d') )
	{
		/* D image selected */
		selected = 'd';
	}
	else if ( $vdas.hasClass('a') )
	{
		/* A image selected */
		selected = 'a';
	}
	else 
	{
		/* S image selected */
		selected = 's';
	}

	if ( $vdas.hasClass('on') )
	{
		/* Hide all off */
		$rows.each(function(){
			var rowSelected = $(this);
			if ( rowSelected.find('.detailsImg.' + selected).hasClass('off') )
			{
				rowSelected.addClass('hide');
				if ( isSelected( rowSelected.attr('id') ) )
				{
					toggleSelected( rowSelected.attr('id') );
				}
			}
		});
	}
	else
	{
		/* Hide all on */
		$rows.each(function(){
			var rowSelected = $(this);
			if ( rowSelected.find('.detailsImg.' + selected).hasClass('on') )
			{
				rowSelected.addClass('hide');
				if ( isSelected( rowSelected.attr('id') ) )
				{
					toggleSelected( rowSelected.attr('id') );
				}
			}
		});
	}
}

function restoreResults () {
	var $rows = $('#results_table tr');
	$rows.each(function(){
		var rowSelected = $(this);
		rowSelected.removeClass('hide');
	});
}

/* Only display the results that are selected */
function displaySelected () {
	var targetId = $('.target').attr('id');
	var $rows = $('#'+targetId + ' table tbody').find('tr');
	/* if something is selected */
	if ( resultsIsSelected() )
	{
		/* Hide all rows not selected */
		$rows.each(function(){
			var row = $(this);
			if ( !(isSelected(row.attr('id') ) ) )
			{
				row.addClass('hide');
			}
		});
	}
	else
	{
		/* UNhide all rows not selected */
		$rows.each(function(){
			var row = $(this);
			if ( !(isSelected(row.attr('id') ) ) )
			{
				row.removeClass('hide');
			}
		});
		$('#resultsDisplayButton').html('Display All');
	}
}

/* example: [Sample Size: Min[20] Max[50]] */
function advancedFilterSampleSize () {
	var min = $('.advanced-search-option-samplesize-min').val();
	var max = $('advanced-search-option-samplesize-max').val();
	var string;

	if (min != "" && max != "")
	{
		string = "[Sample Size:";
		if (min != "")
		{
			string += " Min[" + min + "]";
		}
		if (max != "")
		{
			string += " Max[" + max + "]";
		}
		string += "]";
		return string;
	}
} 

function toggleCreateLogin() 
{
	$createContainer = $('#createLogin');
	$loginContainer	 = $('#login');
	if ($createContainer.hasClass('hide'))
	{
		$loginContainer.stop(true, true).slideUp('fast');
		$createContainer.stop(true, true).slideDown('fast');
		$createContainer.toggleClass('hide');
	}
	else
	{
		$createContainer.stop(true, true).slideUp('fast');
		$createContainer.toggleClass('hide');
		$loginContainer.stop(true, true).slideDown('fast');
		$loginContainer.toggleClass('hide');
	}
	
}

function checkLoginForm()
{
	var email 		= new String( $('#loginEmail').val() );
	var pword		= new String( $('#loginPassword').val() );
	var $error		= $('#login-error').children('p');

	// check if all input is non blank
	if ( !isNonblank( email ) )
	{
		$error.text('Please input login email.');
		return;
	}
	else if ( !isNonblank( pword ) )
	{
		$error.text('Please input login password.');
		return;
	}
	//check if email is of correct form
	else if ( !isEmail( email ) )
	{
		$error.text('Please input a valid email.');
		return;
	}

	//success
	$error.text('');
	//perform account lookup via ajax
	return;

}

function checkNewUserForm()
{
	var email 		= new String( $('#newEmail').val() );
	var pword		= new String( $('#newPassword').val() );
	var comfirm		= new String( $('#newComfirmPassword').val() );
	var $error		= $('#create-login-error').children('p');

	// check if all input is non blank
	if ( !isNonblank( email ) )
	{
		$error.text('Please input login email.');
		return;
	}
	else if ( !isNonblank( pword ) )
	{
		$error.text('Please input login password.');
		return;
	}
	else if ( !isNonblank( comfirm ) )
	{
		$error.text('Please comfirm login password.');
		return;
	}
	//check if email is of correct form
	else if ( !isEmail( email ) )
	{
		$error.text('Please input a valid email.');
		return;
	}

	//success
	$error.text('');
	//perform account lookup via ajax
	return;
}

var isEmail_re       = /^\s*[\w\-\+_]+(\.[\w\-\+_]+)*\@[\w\-\+_]+\.[\w\-\+_]+(\.[\w\-\+_]+)*\s*$/;
function isEmail (s) {
   return String(s).search (isEmail_re) != -1;
}
// Check if string is non-blank
var isNonblank_re    = /\S/;
function isNonblank (s) {
   return (String (s).search (isNonblank_re) != -1);
}

function toggleDisplayChildren( listElement )
{
	var divBox = $($(listElement).children('div')[2])
	var image = $($(listElement).children('div')[0]);
	if (image.hasClass('condensed'))
	{
		if ( divBox.hasClass('hide') )
		{
			divBox.stop(true, true).slideDown('fast');
			divBox.toggleClass('hide');
		}

		image.removeClass('condensed');
		image.addClass('expanded');
	}
	else if ( image.hasClass('expanded') )
	{
		if ( !divBox.hasClass('hide') )
		{
			divBox.stop(true, true).slideUp('fast');
			divBox.toggleClass('hide');
		}

		image.removeClass('expanded');
		image.addClass('condensed');
	}
}

function selectAdvancedOption(e) {
	var parent = $(e).parent();
	var unselectAllFlag = false;
	var selectAllFlag = false;
	if ( parent.hasClass('hasChild')  )
	{
		if ( parent.children('.hierarchyParentImg').hasClass('condensed') 
			&& !parent.children('span.advanced-list').hasClass('highlighted') )
		{
			toggleDisplayChildren(parent.get(0));
		}
		else if ( parent.children('.hierarchyParentImg').hasClass('expanded') 
			&& parent.children('span.advanced-list').hasClass('highlighted') )
		{
			toggleDisplayChildren(parent.get(0));
		}
		if ( $(e).parent().children('span.advanced-list').hasClass('highlighted') )
		{
			unselectAllFlag = true;
		}
		else
		{
			selectAllFlag = true;
		}
		$(e).parent().children('span.advanced-list').toggleClass('highlighted');

		var inputs = $(e).parent().find('input');
		for ( var i = 1; i < inputs.size(); i++ )
		{
			if ( unselectAllFlag )
			{
				$(inputs[i]).attr('checked', false);
			}
			else if ( selectAllFlag )
			{
				$(inputs[i]).attr('checked', true);
			}

			var listElement = $(inputs[i]).parent().children('span.advanced-list')
			var img = $(inputs[i]).parent().children('.hierarchyParentImg');

			if ( img.hasClass('condensed') && !listElement.hasClass('highlighted')
				|| img.hasClass('expanded') && listElement.hasClass('highlighted') )
			{
				toggleDisplayChildren(img.parent().get(0));
			}

			if ( !selectAllFlag && !unselectAllFlag || selectAllFlag)
			{
				listElement.addClass('highlighted');
			}
			else if ( unselectAllFlag )
			{
				listElement.removeClass('highlighted');
			}
			else
			{
				listElement.Class('highlighted');
			}
		}

	}
	else
	{
		$(e).parent().children('span.advanced-list').toggleClass('highlighted');
	}
}

if (!String.prototype.trim) {
 String.prototype.trim = function() {
  return this.replace(/^\s+|\s+$/g,'');
 }
}

function VariableResult(rowId,phen_id,study,dataset_id,dataset,var_name,description,datatype,units,min,max)
{
	//Attributes
	this.rowId = rowId;
	this.phen_id = phen_id;
	this.study = study;
	this.dataset_id = dataset_id;
	this.dataset = dataset;
	this.var_name = var_name;
	this.description = description;
	this.datatype = datatype;
	this.units = units;
	this.min = min;
	this.max = max;

	//methods
	this.remove 				= remove;
	this.importVariableResult 	= importVariableResult;
	this.setRowId 				= setRowId;

	function importVariableResult ()
	{
		resultsVariables.addVariable(this);
	}

	function remove()
	{
		for ( var i = 0; i < resultsVariables.length ; i++ )
		{
			if ( resultsVariables[i] === this )
			{
				resultsVariables.splice(i,1);
				return;
			}
		}
	}

	function setRowId( id )
	{
		this.rowId = id;
	}
}

function ResultsVariables()
{
	this.variables = new Array();

	this.getVariableResult 	= getVariableResult;
	this.addVariable		= addVariable;
	this.appendVariable		= appendVariable;
	this.addAllVariables 	= addAllVariables;

	function addAllVariables () 
	{
		var $row = $('#variables_table tbody').find('tr');
		if ( $row.size() == 0 )
		{
			//Add a row that says No Results
			$('#variables_table').after("<h4 style='color:grey;margin-left:350px;'>No Results</h4>");
			return;
		}

		for ( var i = 0; i < $row.size(); i++)
		{

			var rowId 				= $($row[i]).attr('id');
			var highlight 			= $($row[i]).children('.highlight2').text().split(';');
			var phen_id				= highlight[0];
			var study 				= highlight[1];
			var dataset_id 			= highlight[2];
			var dataset 			= highlight[3];
			var var_name			= highlight[4];
			var description			= highlight[5];	
			var datatype			= highlight[6];
			var units				= highlight[7];
			var min 				= highlight[8];
			var max 				= highlight[9];

			 var selectedVariable = new VariableResult(rowId,phen_id,study,dataset_id,dataset,var_name,description,datatype,units,min,max);

			this.addVariable(selectedVariable);
		}	

	}

	function addVariable ( variable )
	{
		this.variables.push(variable);
		//variable.setRowId("variables_tablerow_"+ (this.variables.length - 1));
		//this.appendVariable(this.variables.length - 1);
	}

	function getVariableResult ( rowId ) 
	{

		for ( var i = 0; i < this.variables.length; i++ )
		{
			if ( this.variables[i].rowId == rowId )
			{
				return this.variables[i];
			}
		}

		return null;
	}

	function appendVariable(i) 
	{
		var variableObject = this.variables[i];

		var rowId 				= variableObject.rowId;
		var study 				= variableObject.study;
		var id 					= variableObject.id;
		var name 				= variableObject.name;
		var description 		= variableObject.description;
		var category 			= variableObject.category;
		var dataSet 			= variableObject.dataSet;
		var dataType			= variableObject.dataType;
		var unitsOfMeasurement	= variableObject.units;
		var mappingSoi			= variableObject.soi;
		var mappingTop 			= variableObject.top;

		var htmlString = "<tr id='"+rowId+"'>"
						+"	<td><input type='checkbox' class='variables_tablerow_checkbox' id='"+rowId+"' /></td>"
						+"	<td class='study'>"+
								study
						+"	</td>"
						+"	<td class='name'>"
						+"		<div class='id'>"+
									id
						+"		</div>"
						+"		<div class='var_name'>"+
									name
						+"		</div>"
						+"	</td>"
						+"	<td class='description'>"+
								description
						+"	</td>"
						+"	<td class='category'>"+
								category
						+"	</td>"
						+"	<td class='dataset'>"+
								dataSet
						+"	</td>"
						+"</tr>";

		$('#variables_table tbody').append(htmlString);
	}
}

/*
function autoAddVariableExamples()
{									

	var study = "Chronic Renal Insufficiency Cohort Study (CRIC)";
	var id = "phv00173276.v1.p1";
	var name = "asthma";
	var description = "History of Asthma or Reactive Airway Disease"
	var category = "";
	var dataSet = "CRIC_Subject_Phenotypes";
	var dataType = "Data Type";
	var units = "Units"
	var max = "100";
	var min = "10";
	var soi = "id454";
	var top = "454id";

	var newVariable1 = new VariableResult(study,id,name,description,category,dataSet,dataType,units,max,min,soi,top);
	newVariable1.importVariableResult();
	var newVariable4 = new VariableResult(study,id,name,description,category,dataSet,dataType,units,max,min,soi,top);

	study = "Genotype-Tissue Expression (GTEx)";
	id = "phv00169056.v2.p1";
	name = "SUBJID";
	description = "Subject ID, GTEx Public Donor ID"
	category = "Link";
	dataSet = "GTEx_Subject";
	dataType = "Data Type2";
	units = "Metric"
	max = "220";
	min = "10";
	soi = "id11";
	top = "111id";

	var newVariable2 = new VariableResult(study,id,name,description,category,dataSet,dataType,units,max,min,soi,top);
	newVariable2.importVariableResult();

	var newVariable5 = new VariableResult(study,id,name,description,category,dataSet,dataType,units,max,min,soi,top);

	study = "Genotype-Tissue Expression (GTEx)";
	id = "phv00169057.v2.p1";
	name = "CONSENT";
	description = "Consent Status"
	category = "Link, Link";
	dataSet = "GTEx_Subject";
	dataType = "Data Type3";
	units = "Metric"
	max = "102";
	min = "40";
	soi = "id33";
	top = "123id";
											
	var newVariable3 = new VariableResult(study,id,name,description,category,dataSet,dataType,units,max,min,soi,top);
	newVariable3.importVariableResult();

	var newVariable6 = new VariableResult(study,id,name,description,category,dataSet,dataType,units,max,min,soi,top);

	newVariable4.importVariableResult();
	newVariable5.importVariableResult();
	newVariable6.importVariableResult();
}
*/

function getAdvancedOptionsBufferStrings () {

	var result = "";
	var selected;

	selected = getSampleSizeOption ();
	result += selected;
	selected = getAgeOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getStudySubjectOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getEthnicityOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getIRBOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getConsentOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getNationalityOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getAnalysisMethodsOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getSexOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getStudyDesignOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getRaceOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getSpecimenTypesOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getPlatformsOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getMachineOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getDataAnalysisMethodsOption ();
	if ( result != "" && selected != "" ) {result += "AND "; }
	result += selected;
	selected = getSequencingTechniquesOption ();

	return result;
}

function getPlatformsOption () 
{
	var checkBoxes = $('#advanced-search-option-platforms').find("input[type=checkbox]:checked");
	var categoryString = "[Platform] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}

function getMachineOption () 
{
	var checkBoxes = $('#advanced-search-option-machine').find("input[type=checkbox]:checked");
	var categoryString = "[Machine] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}

function getDataAnalysisMethodsOption () 
{
	var checkBoxes = $('#advanced-search-option-dataAnalysisMethods').find("input[type=checkbox]:checked");
	var categoryString = "[DataAnalysisMethod] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}

function getSequencingTechniquesOption () 
{
	var checkBoxes = $('#advanced-search-option-sequencingTechniques').find("input[type=checkbox]:checked");
	var categoryString = "[SequencingTechnique] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}

function getStudySubjectOption () 
{
	var checkBoxes = $('#advanced-search-option-studySubject').find("input[type=checkbox]:checked");
	var categoryString = "[StudySubject] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getConsentOption () 
{
	var checkBoxes = $('#advanced-search-option-consent').find("input[type=checkbox]:checked");
	var categoryString = "[Consent] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getAnalysisMethodsOption () 
{
	var checkBoxes = $('#advanced-search-option-analysisMethods').find("input[type=checkbox]:checked");
	var categoryString = "[AnalysisMethod] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getRaceOption () 
{
	var checkBoxes = $('#advanced-search-option-race').find("input[type=checkbox]:checked");
	var categoryString = "[Race] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getStudyDesignOption () 
{
	var checkBoxes = $('#advanced-search-option-studyDesign').find("input[type=checkbox]:checked");
	var categoryString = "[StudyDesign] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getSexOption () 
{
	var checkBoxes = $('#advanced-search-option-sex').find("input[type=checkbox]:checked");
	var categoryString = "[Sex] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getNationalityOption () 
{
	var checkBoxes = $('#advanced-search-option-nationality').find("input[type=checkbox]:checked");
	var categoryString = "[Nationality] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getIRBOption () 
{
	var checkBoxes = $('#advanced-search-option-irb').find("input[type=checkbox]:checked");
	var categoryString = "[IRB] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getSpecimenTypesOption () 
{
	var checkBoxes = $('#advanced-search-option-specimenTypes').find("input[type=checkbox]:checked");
	var categoryString = "[SpecimenType] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getEthnicityOption () 
{
	var checkBoxes = $('#advanced-search-option-ethnicity').find("input[type=checkbox]:checked");
	var categoryString = "[Ethnicity] ";
	var result;

	result = getOptionCheckBoxStrings ( checkBoxes, categoryString );

	return result;
}
function getOptionCheckBoxStrings ( checkboxList, categoryString )
{
	var result = "";

	if ( checkboxList.size() == 0 )
	{
		return "";
	}

	result += "( ";

	for ( var  i = 0; i < checkboxList.size(); i++ )
	{
		if ( $(checkboxList[i]).parent().children('.advanced-list').attr('id') == "Other" )
		{
			result += $(checkboxList[i]).parent().children('input[type=text]').val()
			if ( result != "" )
			{
				result += categoryString;
			}
		}
		else
		{
			result += $(checkboxList[i]).parent().children('.advanced-list').text().trim()
				+ categoryString;
		}
		if ( i < checkboxList.size() - 1 )
		{
			result += "OR ";
		}
	}
	result += ") ";
	return result;
}
function getSampleSizeOption () {
	/* check for selected, else return*/
	if ( $('#' + "advanced-search-option-samplesize").find("input[type=checkbox]:checked").size() == 0 )
	{
		return "";
	}

	var categoryString = "[SampleSize] ";
	var result;

	var min;
	var max;
	//Interval
	min = $("#advanced-search-option-samplesize-min" ).val();
	if ( !($("#sizeMin").is(':checked')) || min == "" )
	{
		min = "*";
	}
	max = $("#advanced-search-option-samplesize-max" ).val();
	if ( !($("#sizeMax").is(':checked')) || max == "" )
	{
		max = "*";
	}
	result = "("+min+","+max+")";

	return result + categoryString;
}
function getAgeOption () {
	/* check for selected, else return*/
	if ( $('#' + "advanced-search-option-age").find("input[type=checkbox]:checked").size() == 0 )
	{
		return "";
	}

	var categoryString = "[Age] ";
	var result;

	var min;
	var max;
	//Interval
	min = $("#advanced-search-option-age-min" ).val();
	if ( !($("#ageMin").is(':checked')) || min == "" )
	{
		min = "*";
	}
	max = $("#advanced-search-option-age-max" ).val();
	if ( !($("#ageMax").is(':checked')) || max == "" )
	{
		max = "*";
	}
	result = "("+min+","+max+")";

	return result + categoryString;
}

function fillMotherTooltipBody(id)
{
	var info = $('#' + id).find('.node-info').text().split(';');
	var studyId;
	var studyName;
	var content = "<table class='recentlyAdded'><thead><th>Daughter Id</th><th>Daughter Study</th></thead>";
	for ( var i = 0; i < info.length - 1; i = i + 2 )
	{
		studyId = info[i];
		studyName = info[i+1];
		content += "<tr><td><a href='#'>"+studyId+"</a></td><td><a href='#'>"+studyName+"</a></td></tr>";
	}
	return content;
}

function fillDaughterTooltipBody(id)
{
	var info = $('#' + id).find('.node-info').text().split(';');
	var studyId;
	var studyName;
	var content = "<table class='recentlyAdded'><thead><th>Mother Id</th><th>Mother Study</th></thead>";
	for ( var i = 0; i < info.length - 1; i = i + 2 )
	{
		studyId = info[i];
		studyName = info[i+1];
		content += "<tr><td><a href='#'>"+studyId+"</a></td><td><a href='#'>"+studyName+"</a></td></tr>";
	}

	return content;
}

function turnOffVWhen0 () 
{
	$tablerows = $('#results_table').find('tr');
	$tablerows.each(function(e){
		var strnum = $(this).find('.PhenNum').text();
		if ( parseInt(strnum) == 0 )
		{
			var v = $(this).find('.detailsImg.v');
			v.removeClass('on');
			v.addClass('off');
		}
	});
}

function resultsStudysCheck()
{
	if ( !$('#results_table') )
	{
		console.log("doh");
		return;
	}

	$tablerows = $('#results_table tbody').find('tr');
	if ( $tablerows.size() == 0 )
	{
		console.log("doh1");
		//Add a row that says No Results
		$('#results_table').after("<h4 style='color:grey;margin-left:350px;'>No Results</h4>");
	}
}

function detectBrowserCompatibilityIssue(BrowserDetect) {
	var browserName = BrowserDetect.browser;
	switch ( browserName )
	{
		case "MSIE": uncompatibleBrowserSolution(browserName); break;
	}
}

function uncompatibleBrowserSolution (browserName) {
	var html = "<div class='container border rounded shadow' style='margin-top:15%;margin-left:30%;width:500px;padding:10px;background-color:#FFE8C5;color:'>"
		+	"<p style='text-align:center;'>This website does not support your current browser.</br>" 
		+	"This website is optimized for Google Chrome.</br>"
		+	"Download Google Chrome <a href='https://www.google.com/intl/en/chrome/browser/'>here</a>.</br>"
		+	"We apologize for the inconvenience.</br></p></div>";
	
	var $body = $('body').html(html);
}