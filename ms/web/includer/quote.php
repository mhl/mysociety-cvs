<?php

	//includes
    require_once dirname(__FILE__) . "/../../../phplib/evel.php";
	
	//sent?
	$sent = false;

	//get the product type
	$product_type = "default";
	if(isset($_GET['p']) && $_GET['p'] != ''){
		$product_type = $_GET['p'];
	}

	//if posting back, then send the email
	if(isset($_POST['_is_postback']) && $_POST['_is_postback'] != ''){

		//email details
		$to = "richard@mysociety.org";
		$from_email = $_POST['txtEmail'];		
		$from_name = $_POST['txtName'];				
		$subject = "[mySociety Quote Request] " .  $_POST['hidProduct'];
		if(isset($_POST['txtOrganisation']) && $_POST['txtOrganisation'] != ''){
			$subject = $subject . ' - ' . $_POST['txtOrganisation'];
		}

		//build up body
		$body = "Product: " . $_POST['hidProduct'] . '\n';
		$body .= "Name: " . $_POST['txtName'] . '\n';
		$body .= "Email: " . $_POST['txtEmail'] . '\n';		
		$body .= "Organisation: " . $_POST['txtOrganisation'] . '\n';		
		if ($product_type == 'map') {
			$body .= "Purpose: " . $_POST['txtPurpose'] . '\n';							
			$body .= "Maximum travel time: " . $_POST['txtMaximum'] . '\n';										
			$body .= "Centre point: " . $_POST['txtCentre'] . '\n';													
			$body .= "Type (interactive/print): " . $_POST['radType'] . '\n';																
			$body .= "Special requests: " . $_POST['txtCentre'] . '\n';			
			$body .= "Special requests: " . $_POST['txtRequests'] . '\n';																
		}

		//send
		evel_send(array(
	            '_body_' => $body,
	            'To' => $to,
	            'From' => array($from_email, $from_name),
	            'Subject' => $subject,
	        ), $to);

		$sent = true;

	}

?>


		<div class="contentfull">
			<h1>Request a quote</h1>
			
			<?php if($sent == false) { ?>
				<form method="POST">
					<fieldset>
						<input type="hidden" name="_is_postback" value="1"/>
						<input type="hidden" name="hidProduct" value = "<?php print $product_type ?>"/>
					</fieldset>
				
					<ul class="nobullets form">
						<li>
							<label for="txtName">Name *</label>
							<input type="text" class="textbox large" id="txtName" name="txtName" />
						</li>
						<li>
							<label for="txtEmail">Email *</label>
							<input type="text" class="textbox large" id="txtEmail" name="txtEmail" />
						</li>
						<li>
							<label for="txtOrganisation">Organisation</label>
							<input type="text" class="textbox large" id="txtOrganisation" name="txtOrganisation" />
						</li>
						<?php if ($product_type == 'map') {?>
							<li>
								<label for="txtPurpose">Purpose</label>
								<input type="text" class="textbox large" id="txtPurpose" name="txtPurpose" />
								<small>i.e. what do you need the map for</small>
							</li>
							<li>
								<label for="txtMaximum">Maximum travel time</label>
								<input type="text" class="textbox small" id="txtMaximum" name="txtMaximum" />
							</li>
							<li>
								<label for="txtCentre">Centre point of map</label>
								<input type="text" class="textbox large" id="txtCentre" name="txtCentre" />
							</li>
							<li>
								<label>Type of map</label>
								<fieldset>
									<input type="radio" name="radType" value="print"/>
									<label class="radiolabel">Print </label>
									<input type="radio" name="radType" value="interactive"/>						
									<label class="radiolabel">Interactive</label>
									<input type="radio" name="radType" value="both"/>												
									<label class="radiolabel">Both</label>
								</fieldset>
							</li>
							<li>
								<label for="txtRequests">Special requests</label>
								<textarea id="txtRequests">
						
								</textarea>
								<small>i.e. 'no tube' or 'with houseprices'</small>
							</li>
						<?php } ?>
					</ul>
					<div class="buttons">
						<input type="submit" value="Request quote" />
					</div>
				</form>
				
			<?php }else{ ?>
				
				<div class="contentfull">
					<p>
						Thanks, your request has been sent and someone will get back to you soon.
						<br/>
						<a href="/">Click here to return to the mySociety homepage</a>
					</p>
				</div>
				
			<?php } ?>
		</div>
