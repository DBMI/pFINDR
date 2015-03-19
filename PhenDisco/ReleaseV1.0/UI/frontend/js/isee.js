/**
 * Created by Dexter Friedman, March 5th, 2015
 *
 * This file contains all of the javascript logic for the iSee
 * intelligient search expansion page. This includes, primarilly
 * tooltip triggering and rendering the study universe as an SVG
 * using the D3 library.
 *
 * Dependencies:
 *   isee-demo-data.json - has included a list of objects, 'demoData'
 *   jquery
 */

if ( demoData === undefined ) {
	throw new Error("demoData is not defined, please include isee-demo-data.json.");
}
else {
	// Define a namespace called ISEE which will keep track of any variables
	// we might need in this script. This is to ensure we don't overwrite any
	// global state that might be left over from the legacy code
	ISEE = {

		/* Constants */

		width: 0,  /* Width of the study graph canvas (auto detected) */
		height: 0, /* Height of the study graph canvas (auto detected) */
		svgContainerID: "#isee-svg", 
		tooltipID: "#isee-node-meta-tooltip",
		anchorStudy: demoData[0].title, /* Name of the root study */
		defaultNodeStrokeColor: '#FBB117',
		defaultNodeColor: '#FFE8C5',
		lineColor: '#024A68',
		defaultRadius: 15,

		/* State of the application */
		currentScenario: 0, /* 0, 1, or 2 (only relevant for the demo) */
		diseaseParameter: 0,
		ageParameter: 0,
		genderParameter: 0,
		raceParameter: 0,
		designParameter: 0,
		childStudies: 0,

		/* SVG References */

		svg: null, /* Reference to the top level svg container */
		/* Callback which will change what is drawn to the SVG if the similarity parameters
		   are modified by the user. */
		svgRefreshCallback: function() { throw new Error('svgRefreshCallback not defined!') },

		studyNodeList: [], /* Contains a list of all the 'circle' svg elements that represent nodes */
		centerNode: null
	};
}

$(document).ready(function(){

	/* By default, all similarity parameters are included and are each considered most relevant */

	$('#diseaseInclude').prop('checked',true); $('#ageInclude').prop('checked',true); $('#designInclude').prop('checked',true);
	$('#genderInclude').prop('checked',true); $('#raceInclude').prop('checked',true);
	$('#diseaseImportant').prop('checked',true);
	$('#ageImportant').prop('checked',true);
	$('#genderImportant').prop('checked',true);
	$('#raceImportant').prop('checked',true);
	$('#designImportant').prop('checked',true);

	ISEE.diseaseParameter = $('input[name="diseaseParameter"]:checked').val();
	ISEE.ageParameter = $('input[name="ageParameter"]:checked').val();
	ISEE.raceParameter = $('input[name="raceParameter"]:checked').val();
	ISEE.genderParameter = $('input[name="genderParameter"]:checked').val();
	ISEE.designParameter = $('input[name="designParameter"]:checked').val();

	$('#isee-study-title').text(demoData[0].title);

	/* Update the ISEE object whenever we change a similarity parameter */

	$('input[name="diseaseParameter"]').change(function(){
		ISEE.diseaseParameter = $('input[name="diseaseParameter"]:checked').val();
		ISEE.svgRefreshCallback();
	});
	$('input[name="ageParameter"]').change(function(){
		ISEE.ageParameter = $('input[name="ageParameter"]:checked').val();
		ISEE.svgRefreshCallback();
	});
	$('input[name="raceParameter"]').change(function(){
		ISEE.raceParameter = $('input[name="raceParameter"]:checked').val();
		ISEE.svgRefreshCallback();
	});
	$('input[name="genderParameter"]').change(function(){
		ISEE.genderParameter = $('input[name="genderParameter"]:checked').val();
		ISEE.svgRefreshCallback();
	});
	$('input[name="designParameter"]').change(function(){
		ISEE.designParameter = $('input[name="designParameter"]:checked').val();
		ISEE.svgRefreshCallback();
	});
	$(ISEE.tooltipID).css('display','none');

	/* Set SVG properties for the study universe graph */

	ISEE.width = Number.parseInt($(ISEE.svgContainerID).css('width')); // auto-detect width & height
	ISEE.height = Number.parseInt($(ISEE.svgContainerID).css('height'));

	var width = ISEE.width;
	var height = ISEE.height;

	/* Once the page has been loaded, we need to start drawing the SVG */
	ISEE.svg = d3.select(ISEE.svgContainerID).append("svg").attr("width", width).attr("height", height);

	var centerX = (width / 2);
	var centerY = (height / 2); // Location of the central node

	/* Define a set of useful functions for dealing with SVG elt creation & deletion */

	ISEE.createNode = function(x,y,radius,fillColor,strokeColor) {

		/* Creates a study node at an arbitrary location (x,y) with given radius */
		/* fillColor and strokeColor are strings, defining the fill/line color of the node */
		/* studyIndex is the index of the given study's metadata in demoData[] */

		fillColor = fillColor || ISEE.defaultNodeColor; // Set a default
		strokeColor = strokeColor || ISEE.defaultNodeStrokeColor; // Set a default
		radius = radius || ISEE.defaultRadius;
		// studyIndex = ( studyIndex == undefined ? 0 : studyIndex ); 
		var newCircle = ISEE.svg.append("circle")
			.attr('cx',x)
			.attr('cy',y)
			.attr('r',radius)
			.attr('fill',fillColor)
			.attr('stroke',strokeColor)
			.attr('stroke-width',3);
		// newCircle.studyIndex = studyIndex;
		ISEE.studyNodeList.push( newCircle );

		/* Set up event listener for the tooltip */
		newCircle.on('mouseenter',function studyMouseEnterFunc(){
			var tooltip = $(ISEE.tooltipID);
			console.log('Mouse enter')
			tooltip.css('position','absolute')
			       .css('left',String(event.pageX) + 'px')
			       .css('top',String(event.pageY) + 'px');
			var studyIndex = -1; // Default return val of indexOf

			// This loop goes through the study node list and attempts to retrieve the index
			// of the node experiencing this event in ISEE.studyNodeList. It is crucial for
			// finding which metadata to pull from demoData
			for ( var i = 0; i < ISEE.studyNodeList.length; ++i ) {
				if ( studyIndex >= 0 ) break;
				else if ( ISEE.studyNodeList[i][0][0] == this ) {
					// The extra [0][0] has to deal with how D3 does collections
					studyIndex = i;
					break;
				}
			}

			if ( studyIndex > -1 ) {
				// THIS IS WHERE THE BUG WAS
				var obj;
			
				// Do logic to figure out index from scenario
				if ( ISEE.currentScenario == 0 ) {
					// The last node in study node list is always the root because that's the way SVG rendering works
					if ( studyIndex + 1 > ISEE.studyNodeList.length - 1 ) {
						studyIndex = 0
						obj = demoData[ studyIndex ]
					}
					else {
						// Otherwise, the index of the study metadata in demoData is the index of the study node
						// in the node list plus 1 (to offset the position of the root node @ 0 in demoData)
						studyIndex++
						obj = demoData[ studyIndex ]
					}
				}
				else if ( ISEE.currentScenario == 1 ) {
					if ( studyIndex + 1 > ISEE.studyNodeList.length - 1 ) {
						// If our study node list index is the last element in our node list, it is the root element
						// (at index zero in the demoData array)
						studyIndex = 0
						obj = demoData[ studyIndex ]
					}
					else {
						// Otherwise, we need to iterate through the portion of the node list that is only child studies.
						// The child studies are ordered in highest -> lowest by ranking, which means that we can search
						// for the corresponding metadata object in demoData by comparing the value of the ranking for the
						// given scenarion. 'i' here is the index of a child node in the list. Since the root node is always
						// last, technically i + 1 is the correct ranking for this study.
						for (var i = 0; i < ISEE.studyNodeList.length; ++i) {
							if (i == studyIndex + 1) {
								// Rankings in the demoData start from 1, so even if we're the i^th child in the node list
								// we are actually the (i + 1)th ranking in demoData. The next for loop searches through all
								// the objects in demoData, and attempts to find which
								for (var indx in demoData) {
									if ( demoData[indx].scenario1 != null && demoData[indx].scenario1 == studyIndex + 1 ) {
										obj = demoData[indx];
										break;
									}
								}
								break;
							}
						}
					}
				}
				else if ( ISEE.currentScenario == 2 ) {
					if ( studyIndex + 1 > ISEE.studyNodeList.length - 1 ) {
						studyIndex = 0
						obj = demoData[ studyIndex ]
					}
					else {
						for (var i = 0; i < ISEE.studyNodeList.length; ++i) {
							if (i == studyIndex + 1) {
								for (var indx in demoData) {
									if ( demoData[indx].scenario2 != null && demoData[indx].scenario2 == i ) {
										obj = demoData[indx];
										break;
									}
								}
								break;
							}
						}
					}
				}

				$('#isee-title-tooltext').text(obj.title);
				$('#isee-study-id-tooltext').text(obj.studyID);
				$('#isee-disease-tooltext').text(obj.disease);
				$('#isee-age-tooltext').text(obj.age);
				$('#isee-gender-tooltext').text(obj.gender);
				$('#isee-race-tooltext').text(obj.race);
				$('#isee-study-tooltext').text(obj.studyDesign)
				tooltip.show();
			}
		});
		newCircle.on('mouseleave',function studyMouseLeaveFunc(){
			// console.log('Mouse leave')
			$(ISEE.tooltipID).hide();
		});

		return newCircle; // Returns a D3 svg object, which we can add event listeners to
	};
	ISEE.createChildStudy = function(simScore) {

		/* Creates a child study node, centered around the middle of the SVG, with a distance
		   to the center of simScore (times some constant) */

		if ( simScore == null || simScore < 0 ) {
			return; // We don't include this node in this scenario
		}

		var radius = simScore * 30 + 30;
		var thetaInc = 360 / demoData.length;
		var theta = thetaInc * ISEE.childStudies;
		theta = theta * Math.PI / 180;

		// Draw a line before we add the circles
		ISEE.svg.append("line").attr('x1',centerX).attr('y1',centerY)
			.attr('x2', radius * Math.cos(theta) + centerX )
			.attr('y2', radius * Math.sin(theta) + centerY )
			.attr('stroke', ISEE.lineColor)
			.attr('stroke-width', 3);

		var studyNode = ISEE.createNode( radius * Math.cos(theta) + centerX, radius * Math.sin(theta) + centerY, ISEE.defaultRadius * .75, null, null);//, ISEE.childStudies);
		ISEE.childStudies++;

		return studyNode; // Follows pattern of returning the d3 element, like ISEE.createNode()
	};
	ISEE.clearSVG = function() {
		ISEE.svg.selectAll("*").remove();
		ISEE.childStudies = 0; // Reset child counter
		ISEE.studyNodeList = []; // Clear node list
	};

	/* Set up the rows in the nearest studies table */
	ISEE.refreshNearestStudies = function() {
		var tbody = $('#nearest-studies-tbody');
		var tr = null; var td = null;
		tbody.empty(); // Don't overdraw the rows

		// Remember, demoData[0] is the root/anchor study, so including it here is nonsense
		for ( var i = 1; i < demoData.length; ++i) {
			var text = demoData[i].studyID + " " + demoData[i].title;
			switch (ISEE.currentScenario) {
				// Reverse case order so that we default to case 0
				case 2:
					if ( demoData[i].scenario2 > 0 ) {
						tbody.append("<tr>");
						tr = tbody.children().last();
						td = tr.append("<td>").children().last();
						td.addClass("title");
						td.text(text);
					}
				break;
				case 1:
					if ( demoData[i].scenario1 > 0 ) {
						tbody.append("<tr>");
						tr = tbody.children().last();
						td = tr.append("<td>").children().last();
						td.addClass("title");
						td.text(text);
					}
				break;
				default:
				case 0:
					if ( demoData[i].simStudyRating > 0 ) {
						tbody.append("<tr>");
						tr = tbody.children().last();
						td = tr.append("<td>").children().last();
						td.addClass("title");
						td.text(text);
					}
				break;
			}
		}
	};

	/* Update the elements we have whenever the svgRefreshCallback() is called */
	ISEE.svgRefreshCallback = function() {
		var prevScenario = ISEE.currentScenario;
		console.log("Similarity parameters have been changed: " + [
			ISEE.diseaseParameter, ISEE.ageParameter, ISEE.genderParameter,
			ISEE.raceParameter, ISEE.designParameter
		]);
		if ( ISEE.diseaseParameter == 0 && ISEE.ageParameter == 0 && ISEE.genderParameter == 0  &&
		          ISEE.raceParameter == 0  && ISEE.designParameter != 0 ) {
			ISEE.currentScenario = 1;
		}
		else if ( ISEE.diseaseParameter == 0 && ISEE.ageParameter == 0 && ISEE.genderParameter == 0  &&
		          ISEE.raceParameter != 0  && ISEE.designParameter == 0 ) {
			ISEE.currentScenario = 2;
		}
		else {
			ISEE.currentScenario = 0; // bad but should work for now
		}

		if ( prevScenario != ISEE.currentScenario ) {
			ISEE.clearSVG();
			ISEE.generateStudyUniverse();
		}
		console.log("We are in scenario: " + ISEE.currentScenario);
	};

	/* Set up all of the SVG elements we will need */
	ISEE.generateStudyUniverse = function(){
		/* Assumes an empty svg element, or that ISEE.clearSVG() has been called */

		// Draw center node on top of all the lines

		// Generate the child studies
		for ( var i = 1; i < demoData.length; ++i) {
			switch (ISEE.currentScenario) {
				// Reverse case order so that we default to case 0
				case 2:
					if ( demoData[i].scenario2 > 0 && demoData[i].scenario2 != "anchor" )
						ISEE.createChildStudy(demoData[i].scenario2);
					break;
				case 1:
					if ( demoData[i].scenario1 > 0 && demoData[i].scenario1 != "anchor" )
						ISEE.createChildStudy(demoData[i].scenario1);
					break;
				default:
				case 0:
					if ( demoData[i].simStudyRating > 0 && demoData[i].simStudyRating != "anchor" )
						ISEE.createChildStudy(demoData[i].simStudyRating);
					break;
			}
		}

		// Draw center node on top of all the lines
		ISEE.centerNode = ISEE.createNode(centerX, centerY, ISEE.defaultRadius, null, null);
	
		// Reset the nearest studies table in accordance with the new scenario
		ISEE.refreshNearestStudies();
	};
	ISEE.generateStudyUniverse();

});