# slack-media-extraction
A simple script meant to extract images, namely screenshots, from slack exports (json files).
The screenshots could have been uploaded to slack, but most where Steam links and this script downloads all of them.
The script also sets the creation date of the file to the date that the file was posted.

## Execution
I just paste it into [DreamPie](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwijlJ_qh5DaAhVSWsAKHciMAIkQFggoMAA&url=http%3A%2F%2Fwww.dreampie.org%2F&usg=AOvVaw2IoJEmZ71rNOyQV1nOb1O1), change the arguments at the bottom and run.

### Requirements:
Depends on:
  * `requests`
  * `rfc6266`
