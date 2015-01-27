$(document).ready(function(){
	var $popUp = $('#definitionTooltip');
    var offset = {x: -520, y: 0}; // tooltip offset from the cursor'
    var pageHeight;

	$('#variables_table td.category span').mouseover(function(event) {
	    //display tooltip
	    pageHeight = $(document).height();
	    $popUp.show();
	}).mousemove(function(e) { // move
	    // set the positioning with offset
	    if ( (e.pageY + $popUp.height()) > pageHeight )
	    {
	    	var difference = (e.pageY + $popUp.height()) - pageHeight;
	    	var newY = e.pageY - difference;
	    	$popUp.css({left: e.pageX + offset.x, top: newY});
	    }
	    else
	    {
	    	$popUp.css({left: e.pageX + offset.x, top: e.pageY });
	    }

	    // set the tooltip HTML contents
	    $popUp.html(
	    	//fill
	    	fillDefinitionToolTip($(this).text())
	    );
	}).mouseout(function() {
	    //hide
	    $popUp.hide();
	});
});

function fillDefinitionToolTip (text)
{
	var string = new String ();
	switch (text)
	{
		case "Demographics": string = "demographics"; break;
		case "Medication Patient":
		case "Medical History": string = "medication";break;
		case "Laboratory Test ": string = "laboratory"; break;
		case "Medical History": string = "medical"; break;
		case "Family History": string = "family"; break;
		case "Mental or Emotional finding": string = "mental"; break;
		case "Smoking History": string = "smoking"; break;
		case "Drinking History": string = "drinking"; break;
		case "Substance Use History": string = "substance"; break;
		case "Daily or Recreational Activity": string = "activity"; break;
		case "Eating or Nutritional finding": string = "nutritional"; break;
		case "Self-care Status": string = "selfcare"; break;
		case "Healthcare Activity Finding": string = "healthcare"; break;
		case "Diagnostic Procedure": string = "diagnostic"; break;
		case "Therapeutic or Preventive Procedure": string = "preventive"; break;
		case "Clinical Attributes": string = "clinical"; break;
		case "Research Attributes": string = "research"; break;
		default: string = "Unkown Category"; break;
	}

	return getDefinition(string);
}

function getDefinition(title)
{
  	var string = new String();

	switch (title) 
	{

	case "demographics": string = '<!-- Demographics  START --> <div><h3>Demographics</h3><dl><dt><b>Demographics (participant)</b></dt><dd>The demographic of the participant (subject) includes variables such as marital status, age, gender, race, ethnicity, education level, employment status, etc. This category is defined loosely to include any variables related to the items listed above.  For example finding variable such as “age first started smoking” is categorized under demographics as well as smoking history…”</dd></dl><p>The same definition goes for either the study participant or the relative (usually under Family, brother, sister etc…) </p><dl><dt><b>Demographics (family/ relative)</b></dt><dd>The family demographic category includes demographic variables of the participant’s family such their age, gender, race, ethnicity, education level, employment status,  etc. This category is also defined loosely to include any variables related to the above variables . For example, “age mother first diagnosed with cancer” and “relative smoking history” will all be categorized under this demographics.</dd></dl><!-- Demographics END --> </div>'; break;

	case "medication": string = '<!-- Medication History  START --> <div> <h3>Medication History </h3><p>This category includes information regarding prescription history, including details for each usage and other drugs related data.</p><dl><dt><b>Medication History of study participant</b></dt><dd>Medication history describes subject’s medication related information</dd><dt><b>Family Medication History</b></dt><dd>This category includes all variables that describe medication related information of family member.</dd></dl><!-- Medication History END --> </div>'; break;

	case "laboratory": string = '<!-- Laboratory Test  START --> <div> <h3>Laboratory Test (subcategories by SOI)</h3><p>In this category, are included information regarding subject/ participant lab tests such as: a blood draw or specimen collection like urine, saliva, stool or body tissues.</p><p>We distinguish 2 lab tests per subject of Identification:</p><ol><li>Laboratory test of the study participant and </li><li>Laboratory test of relative/family of participant</li></ol><h3>Medical History (only for SOI of patient/study subject/participant)</h3><p>The Medical History category describes any patient’s health related problems present and past. It includes any variables that describe study subject’s health status/condition / past conditions. Both physical and mental health status / Conditions are considered. </p><p>FYI, our rule engine takes the concepts of the following semantic types for this category</p><ul style="list-style-type: none;"><li><table border="0"><tr><td>•	disease or syndrome</td><td>dsyn</td></tr><tr><td>•	neoplastic process</td><td>neop</td></tr><tr><td>•	sign or symptom</td><td>sosy</td></tr><tr><td>•	acquired abnormality</td><td>acab</td></tr><tr><td>•	anatomical abnormality</td><td>anab</td></tr><tr><td>•	biologic function</td><td>biof</td></tr><tr><td>•	congenital abnormality</td><td>cgab</td></tr><tr><td>•	finding</td><td></td></tr> <tr><td>•	injury of poisoning</td><td>inpo</td></tr><tr><td>•	organism function</td><td>orgf</td></tr><tr><td>•	pathologic function</td><td>patf</td></tr><tr><td>•	physiological function</td><td>phsf</td></tr><tr><td>•	mental or behavioral dysfunction</td><td>mobd</td></tr></table></li></ul><!-- Laboratory Test END --> </div>'; break;

	case "family": string = '<!-- Family History  START --> <div> <h3>Family History (only for SOI of NON patient or study subject)</h3><p>Variables that describe health status/condition of people other than the participant belong to this category.  Both physical and mental health status/conditions are also considered.  Example is “sibling diagnose with autism”</p><p>FYI, Just like Medical history, our rule engine takes the concepts of the following semantic types for this category</p><ul style="list-style-type: none;"><li><table border="0"><tr><td>•	disease or syndrome</td><td>dsyn</td></tr><tr><td>•	neoplastic process</td><td>neop</td></tr><tr><td>•	sign or symptom</td><td>sosy</td></tr><tr><td>•	acquired abnormality</td><td>acab</td></tr><tr><td>•	anatomical abnormality</td><td>anab</td></tr><tr><td>•	biologic function</td><td>biof</td></tr><tr><td>•	congenital abnormality</td><td>cgab</td></tr><tr><td>•	finding</td><td></td></tr> <tr><td>•	injury of poisoning</td><td>inpo</td></tr><tr><td>•	organism function</td><td>orgf</td></tr><tr><td>•	pathologic function</td><td>patf</td></tr><tr><td>•	physiological function</td><td>phsf</td></tr><tr><td>•	mental or behavioral dysfunction</td><td>mobd</td></tr></table></li></ul><!-- Family History END --> </div>'; break;

	case "mental": string = '<!-- Mental Or Emotional finding  START --> <div> <h3>Mental or Emotional finding (subcategories by SOI)</h3><p>This category is described by variables that are related to emotions, thoughts, feelings, behaviors, mood, and cognitive processes. </p><p>There are 2 components in this category:</p><dl><dt><b>The participant Mental or Emotional finding</b></dt><dd>All variables describing the level of psychological well-being of the participant or his/her emotions fall in this subcategory</dd><dt><b>Relative’s Mental or Emotional finding</b></dt><dd>All variables describing the emotions and/or the level of psychological well-being of the participant’ relative will fall in this subcategory</dd></dl><!-- Mental Or Emotional finding END --> </div>'; break;

	case "smoking": string = '<!-- Smoking History  START --> <div> <h3>Smoking History </h3><p>All variables related to smoking in the present, past and future are part of this category. So, information regarding when started or stopped smoking, are included.</p><p>This category also possesses 2 components:</p><dl><dt><b>The subject/participant smoking history: </b></dt><dd>This category indicates whether the subject is or was a smoker or never smoked. If, he/she quitted, when and how the stopping process took place. </dd><dt><b>Participant relative(s) smoking history: </b></dt><dd>This category indicates whether the subject’s relative(s) (mother, father, siblings… ) was, is a smoker or never smoked; stopped, when and how.</dd></dl><!-- Smoking History END --> </div>'; break;

	case "drinking": string = '<!-- Drinking History  START --> <div> <h3>Drinking History </h3><dl><dt><b>Participant</b></dt><dd>This category includes information about the drinking status of the subject/ participant. It indicates whether the subject drinks alcohol or not, the frequency, and /or whether they stopped, when, how, and/or why.</dd><dt><b>Family / relative</b></dt><dd>This category includes information about the drinking status of the subject/participant. It indicates whether the subject drinks alcohol, the frequency, and /or whether they stopped, when, how and/or why.</dd></dl><!-- Drinking History END --> </div>'; break;

	case "substance": string = '<!-- Substance Use History  START --> <div> <h3>Substance Use History </h3><dl><dt><b>Study participant</b></dt><dd>This category gives present or past information about subject use of addictive substances such as Cocaine, Opiate, Stimulant, Marijuana, Pot or Cannabis</dd><dt><b>Family / relative</b></dt><dd>Present or/and past information about subject’s relative use of addictive substances such as Cocaine, Opiate, Stimulant, Marijuana, Pot or Cannabis are the mainly present in this category</dd></dl><!-- Substance Use History END --> </div>'; break;

	case "activity": string = '<!-- Daily or Recreational Activity  START --> <div> <h3>Daily or Recreational Activity </h3><p>This category measures the functional health of either the participant or their relative except self care. They are described with words like Gait, Walking, exercise, sports, workout, gambling, sleep, toilet, chore, eat out and stand etc…</p><dl><dt><b>Study participant</b></dt><dd>All variables describing the subject’s activities of daily living and / or recreational activities except self-care are included in this category. </dd><dt><b>Relative / Participant</b></dt><dd>All variables describing the subject’s relative activities of daily living and / or recreational activities belong to this category.</dd></dl><!-- Daily or Recreational Activity END --> </div>'; break;

	case "nutrition": string = '<!-- Eating or Nutritional finding  START --> <div> <h3>Eating or Nutritional finding </h3><p>This category describes the subject or their relative(s) eating habits.</p><dl><dt><b>Participant</b></dt><dd>Variables related to food/nutrition consumption of the participant belong to this category</dd><dt><b>Relative/family member</b></dt><dd>Variables related to food/nutrition consumption of subject’s relative such as mother, grand mother … belong to this category</dd></dl><!-- Eating or Nutritional finding END --> </div>'; break;

	case "selfcare": string = '<!-- Self-care Status  START --> <div> <h3>Self-care Status </h3><p>This category measures the ability to perform basic personal care activities and instrumental activities of daily living. Self-care means ability to take care of oneself in the following dressing, grooming, bathing, eating, toileting, hygiene.</p><dl><dt><b>Participant Self-care</b></dt><dd>Variables containing the participant self-care information are in this category.</dd><dt><b>Relative(s) Self-care</b></dt><dd>Variables that describe self-care ability of participant relative belong to this category.  </dd></dl><!-- Self-care Status END --> </div>'; break;

	case "healthcare": string = '<!-- Healthcare Activity Finding  START --> <div> <h3>Healthcare Activity Finding </h3><p>This category describes Healthcare visits such as clinic visit, hospitalization, doctor’s visit appointment, etc.</p><dl><dt><b>Health care Activity finding for study participant </b></dt><dd>Includes all healthcare visit variables related to the study participant</dd><dt><b>Health care Activity finding for family / sibling</b></dt><dd>Includes all healthcare visit variables related to the participant’s relative (mother, father, sister, brother, grand-parents)</dd></dl><!-- Healthcare Activity Finding END --> </div>'; break;

	case "diagnostic": string = '<!-- Diagnostic Procedure  START --> <div> <h3>Diagnostic Procedure </h3><p>This category describes all a procedures in the identification of a disease from its symptoms.  Terms such as: Myocardial Infarction, Inflammation, Cerebrovascular accident, Cholesterol, Heart Diseases, Hypertension, Intermittent Claudication, Obesity, Osteoporosis, risk factors, Smoking … will be included.</p><p>There are 2 components in this category:</p><dl><dt><b>Diagnostic Procedure of study participant</b></dt><dd>All participant related procedures in the identification process of a disease from its symptoms.  </dd><dt><b>Diagnostic Procedure of relative / family</b></dt><dd>Procedures in the identification process of a disease from its symptoms, related to participant relative/family</dd></dl><!-- Diagnostic Procedure END --> </div>'; break;

	case "preventive": string = '<!-- Therapeutic or Preventive Procedure  START --><div> <h3>Therapeutic or Preventive Procedure (subcategories by SOI)</h3><p>Therapeutic procedures are procedures that soothe the patient. Terms like massages, sitting down, and warm bath … are indicative of such procedure</p><p>Preventive procedure on the other hand consists of measures taken to prevent diseases or injuries rather than curing them or treating their symptoms. Terms such as hand-washing, breastfeeding, immunizations, screening tests, family history of a disease, etc… fall in this category.</p><dl><dt><b>Therapeutic or Preventive Procedure to participant</b></dt><dd>Therapeutic procedures and/or Preventive procedures related to the patients. Eg: number of massage sessions</dd><dt><b>Therapeutic or Preventive Procedure to participant’s relative/ family</b></dt><dd>Therapeutic or preventive procedure to participant’s relative / family Eg:  mother’s immunization records, , family history of a cancer, etc… fall in this category.</dd></dl><!-- Therapeutic or Preventive Procedure END --> </div>'; break;

	case "clinical": string = '<!-- Clinical Attributes  START --> <div> <h3>Clinical Attributes </h3><p>This category includes all measurement information (Whole Exome Sequencing, RNA Sequencing, Whole Genome Genotyping, Whole Genome Sequencing), routine assessments, and others. Excluded are all diagnostic procedures in this list.</p><ul style="list-style-type: none;"><li>Gestational age, basal metabolic rate, body surface area, blood pressure, body mass index, body weight, diastolic blood pressure, heart rate, height, respiration rate, systolic blood pressure, temperature, temperature, pulse, respiration, weight, vital sign, Body temperature, pulse rate, systolic pressure, diastolic pressure, resting pressure, pulse pressure, heartbeat, Birth weight, Body fat , istribution, adiposity, waist circumference, waist-hip ratio, head circumference, chest circumference, pulse, Respiratory depth, pulse deficit, pain, oxygen saturation, pupil size, pupil equality, pupil reactivity to light, pulse oximetry, diameter, perimeter, systolic, diastolic, visual acuity </li></ul><!-- Clinical Attributes END --> </div>'; break;

	case "research": string = '<!-- Research Attributes  START --> <div> <h3>Research Attributes </h3><p>All Variables related to research activities belong to this category. For examples, variable descriptions that contain any of following words or semantic type of Research Activity fall in to this category</p><ul><li>Control group</li><li>Control status</li><li>Case</li><li>Case control</li><li>Protocol</li></ul><!-- Research Attributes END --> </div>'; break;

	default: string = "Unknown Category"; break;
	}

	return string;
}