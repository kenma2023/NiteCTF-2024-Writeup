### Web - Cybernotes 
- Prompt: ![](attachments/Pasted%20image%2020241215130415.png)
- The app is just a login screen and "reset password" doesn't have true functionality it just statically links to a xkcd comic ![|260](attachments/Pasted%20image%2020241215130507.png)
- just to satisfy curiosity trying to login as admin, go to the admin endpoint, any basic mishaps, etc doesn't work
- Now inspecting the code + the prompt 2 things spring up, there's 2 named directories of interest:
	- asset - ![](attachments/Pasted%20image%2020241215131319.png)
	- uploads - ![](attachments/Pasted%20image%2020241215131331.png)
- `/assets/` gives nothing, but `/uploads/` was left open and does
	- ![](attachments/Pasted%20image%2020241215131606.png)
- The first log file, "2048-07-21.log", has a username + password, the rest are filler:
	- Username: `D3aDs0ck`, Password: `bluM#_M@y_N3vr`
- Dockerfile is interesting: ![](attachments/Pasted%20image%2020241215133452.png)
	- ENV JWT_SECRET_KEY=H6jga21h1
	- ENV FDRP_JWT_SECRET_KEY=wEdAeLdjae
- After logging in it's good practice to check if anything changed and indeed there's a session token in "Storage --> Local Storage" but most often I see them in "Storage --> Cookies"
- We know it's a Flask app now, so you can decode that token and you'll need to use a resource for it, so **now** the challenge should let you use other resources 
	- For future mileage I recommend using the [burpsuite extension for JWT tokens](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts)
- So keep the standard token, sign it, then resend the **GET /api/notes** request to load up your new notes and voila 
- Flag - nite{7rY_XKcD_S3b_f0R_3xPl4nA7i0n}
- **Explanation:**
	- [JWT Resource](https://jwt.io/introduction)

### Web - Tammy's Tantrums(Unsolved)
#nosql
- You can register and login and get this screen to upload posts 
	- ![|284](attachments/Pasted%20image%2020241218143453.png)
- Given the structure of the website this jumps out as probably some type of XSS, XXE, or SSTI Injection but that's just a guess luckily we have the source code
- In this case Tammy is the admin so we probably have to login as her or leak her data since the flag is most likely a private tantrum
- Most Interesting routes are "app/tantrums/page.tsx" and its backend "app/api/v1/tantrums" which is another 3 routes itself
	- **"app/tantrums/page.tsx"**
		- Both the "create" & "delete" functionality give us errors from the server which could leak data
	- backend: **"app/api/v1/tantrums**
		- **"route.ts"**
			- uses JWT to connect session --> data so to login as Tammy would have to break it which is unlikely
			- New tantrums are not **explicitly** sanitized but isn't an obvious vulnerability either
		- **"/get/route.ts"** - not interesting
		- **"/\[id]/route.ts** - entirely about DELETE functionality
			- There is a template in this finally that we can control  ![](attachments/Pasted%20image%2020241218164740.png)
			- It has instant access to the database which is a MongoDB service as the Dockerfile lets us know
			- Burpsuite [noSQL Injection tutorial](https://portswigger.net/web-security/nosql-injection) which specifically lists the `$where` operator
- Problem - we can find the private tantrum, cannot see it though. 
	- `else if (tantrum.userID != userid) --> error 403` means we successfully found a tantrum matching what we want(title & description most importantly)
- Solution - brute force it
	- The flag is format, "nite{..text..ascii..}" so search for the string "nite{ + \*letter\*" and then continuously append letters to it 
	- While brute forcing if it's an error-404, does not matter; if it's an error-403 then that position + value of the string we're appending to is correct
	- finding a correct letter means expanding the flag from ex: "nite{##"  to  "nite{###" and keep going until string ends 
- Implementation:
	- send "DELETE" requests to this endpoint ![](attachments/Pasted%20image%2020241218181835.png)
	- When we get Error 403 we've found a substring of the flag, the system just won't give it to us directly since we're the wrong user ![](attachments/Pasted%20image%2020241226195909.png)
[Official Writeups + Source Code](https://github.com/Cryptonite-MIT/niteCTF-2024)