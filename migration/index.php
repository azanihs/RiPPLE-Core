<html>
	<head>
		<title>Login to the PeerWise Flashcard Project</title>
		<link rel="stylesheet" href="assets/css/bootstrap.min.css">
		<link rel="stylesheet" href="assets/css/signin.css">
	</head>

	<body>
		<div class="container">
			<h2 class="form-signin-heading text-center">Please sign in to select questions</h2>
			<form class="form-signin" method="POST" action="options.php">
	        	<label for="inputEmail" class="sr-only">Email address</label>
	        	<input name="email" type="email" id="inputEmail" class="form-control" placeholder="Email address" required="" autofocus="">
	        
	        	<label for="inputPassword" class="sr-only">Password</label>
	        	<input name="password" type="password" id="inputPassword" class="form-control" placeholder="Password" required="">
	            
	            <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
	      	</form>
      	</div>
	</body>
</html>