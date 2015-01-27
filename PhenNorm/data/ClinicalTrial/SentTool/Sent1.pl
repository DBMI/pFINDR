#!/usr/local/bin/perl

# Input: Text file
# Output will be a standard IO with one sentence in one line
# Example: run perl Sent1.pl ./CLINIC300.txt


sub  trim { my $s = shift; $s =~ s/^\s+|\s+$//g; return $s };

$filename = $ARGV[0];
open (IN,$filename);

$text_note = '';

$MAX=0;
while (<IN>){
	$text_note.=$_;
	$MAX++;
};

close (IN);

my $peopletitles='Dr|Drs|Mrs?|Miss|Ms|Revs?|Pres|Sen|Hon|MD|PhD|Mr|MPH|CEO';

my $sentence_words='we|us|patient|denies|reveals|no|none|he|she|his|her|they|them|is|was|who|when|where|which|are|be|have|had|has|this|will|that|the|to|in|with|for|an|and|but|or|as|at|of|have|it|that|by|from|on|include';

my $det='a|an|the';

my $prep='about|above|across|after|against|aka|along|and|anti|apart|around|as|astride|at|away|because|before|behind|below|beneath|beside|between|beyond|but|by|contra|down|due to|during|ex|except|excluding|following|for|from|given|in|including|inside|into|like|near|nearby|neath|of|off|on|onto|or|out|over|past|per|plus|since|so|than|though|through|til|to|toward|towards|under|underneath|versus|via|where|while|with|within|without';

@sents = split(/\n/, $text_note);
@Output;
$numsent =@sents;

my ($sent,$nextsent);

#for (my $sentnum=0; $sentnum<= $numsent+2; $sentnum++) {
for (my $sentnum=0; $sentnum<=$MAX+50; $sentnum++) {

    $sent = $sents[$sentnum];

    $nextsent = $sents[$sentnum+1] if $sentnum < $numsent;

    if ($sent=~/temp/i || $sentnum>970) {

        print ;

    }

    # SPLIT a line that contains multiple sentences into multiple lines

    if ($sent=~s/(\b(?:$sentence_words)(?:[^\.]|\d\.\d)*\.\s+)((?:\(?[-\d]{1,2}[.\)]?\s*)?(?:[AI] |[A-Z][A-Z]+.*))$/$1/io      #standard sentence match with or without list identifiers

        ||  ($sent=~s/([\w\/ ]{5,100}\w\.\s+)((?:[AI] |[B-Z][a-z]+)[^.]*(?:$sentence_words).*)$/$1/o) ) {

        my $remainder = $2;

        if ($sent !~ /(?:$peopletitles)\.\s*$/o && $remainder=~/^(?:A |[A-Z][a-zA-Z])/o) { #check to make sure it was a capital
	    
	    $sents[$sentnum] = $sent.' ';

            if ($nextsent=~/^(?:\s*[A-Z]|[\w\s][:-])/o) {

                #add as a new sentence because the next one looks like a tag
		
                splice @sents,$sentnum+1,0,$remainder;    

            } else {

                #combine it with the next sentence

                $sents[$sentnum+1] = $remainder . ' ' .$sents[$sentnum+1];

            }

	    if ($sent =~ /\..*\w/o) {redo; } else { 
		                                    print $sent."\n";
						    next; }

        } else {

            $sent = $sents[$sentnum];

        }

    }
     elsif ($sent=~s/((?:[-\d]{1,2}[.\)]{1,2})\s*[A-Za-z][\w%&\-\. ]+[a-z]\.?\s*)((?:[-\d]{1,2}[.\)]{1,2})\s*[A-Za-z]\w+.*)$/$1/o      #split items in list of format of "1. text... 2. text..."
 
             || $sent=~s/((?:\([-\d]{1,2}[.\)]{1,2})\s*[A-Za-z][\w%&\-\. ]+[a-z]\.?\s*)((?:\([-\d]{1,2}[.\)]{1,2})\s*[\w ]+.*)$/$1/o) {   #split items in list of format of "(1) text... (2) text..."
 
             my $remainder = $2;
 
             $sents[$sentnum] = $sent . ' ';
 
             if ($nextsent=~/^(?:\s*[A-Z]|[\w\s][:-])/o) {
 
                 #add as a new sentence because the next one looks like a tag
 
                 splice @sents,$sentnum+1,0,$remainder;    
 
             } else {
 
                 #combine it with the next sentence
 
                 $sents[$sentnum+1] = $remainder . ' ' .$sents[$sentnum+1];
 
             }
 
             if ($sent =~ /\..*\w/o) {  redo; } else {next;}	    
 
	 }
 
   #COMBINE with next string as it is likely a continuation

     if (length($sent) > 65) {
 
         if ($sent=~/\b(?:$sentence_words)\b/oi && $sent!~/\.\s*$/o) {
 
             if ($nextsent=~/^\s*[a-z]/o || $nextsent=~/^\s*\d+\s*[a-z]+/o || $sent=~/\b(?:$prep|$det)$/oi) {
 
                 $sents[$sentnum] .= ' ' . $nextsent;
 
                 splice @sents, $sentnum+1,1;
 
                 redo;
 
             }
 
 	}
  
     }

	if (length(trim($sents[$sentnum])) > 0) { 
    		print $sents[$sentnum]."\n";
	}

}

