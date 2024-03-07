# Tweeter social network
<sup>For Russle Rossle<sup>

**Our Commands** <br>
<sup>------------------------<sup>

Format - **Command** {input args}: explanation
<br>
  - **create** {}: create the database and its schema, no data is in the database yet <br>
  - **generate** {}: fill the database with users, as well as random follows, random subscriptions, and random blocks <br>
  - **adduser** {email}: add a user <br>
  - **addaccount** {email, username, password}: add an account <br>
  - **followAccount** {followerusername, followeeusername}: have an account follow another account <br>
  - **unfollowAccount** {unfollowerusername, unfolloweeusername}: have an account stop following another account <br>
  - **listUsers** {}: list all users currently registered in the database <br>
  - **listAccounts** {}: list all accounts currently registered in the database <br>
  - **createPost** {username, content, image, hashtag}: create a post for account username, each post contains text (content), the name of an image file (image), and a hashtag <br>
  - **editPost** {content, image, hashtag, post_id}: edit an existing post (post_id) to instead contain text (content), the name of an image file (image), and a hashtag <br>
  - **deletePost** {post_id}: delete a post from the database by its post_id <br>
  - **displayFeed** {account_id}: show posts made by the accounts that user account_id is following <br>
  - **displayRecommendedFollowees** {account_id}: recommends people to follow based on how many of your current followers follow them and gives them a rating based on the number of your following that follows them <br>
  - **displayRecommendedFeed** {account_id}: shows recommended posts made by a recommended followee (described above) <br>
  - **subscriberScore** {}: compares how many subscriptions an account has to how many accounts said account follows and then gives each account in the database a corresponding score. The higher the score, the higher the subscription to following ratio <br>
