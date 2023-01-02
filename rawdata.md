# The original scraped data

These are the original scraped data.

## KYM

This is the raw data from KnowYourMeme.

177 MB

28,799 memes

updated 12.05.2021

### Schema

* Title
* Category - content is separated into categories: people, events, and more, in addition to memes.
* Addition timestamp
* Latest update timestamp
* Template image URL
* Status - representing quality control, for example as confirmed, in research or *deadpool*.
* Origin - meme origin, either as websites or media they are determined to originate from.
* Year
* Type - KnowYourMeme categorizes the memes into distinct types.
* Tags
* Additional references
* Parent - presented as "Part of a series on", representing KnowYourMeme's internal meme taxonomy.
* Siblings - presented as "Related Entries".
* Children - presented as "Related Subentries".
* Search terms - provided in an iFrame to Google Trends.

[Download](https://owncloud.ut.ee/owncloud/index.php/s/g4qB5DZrFEz2XLm)

## ImgFlip

### Schema

[Download](https://owncloud.ut.ee/owncloud/s/mFdPCY2mWdQLZ7Q)

## Google Vision enrichment

Contains the query results after running all of the meme template images through Google Vision.

374 MB

419,002 labels

197,582 entities

updated 15.05.2021

### Schema

* Label annotations
  * mid - URI
  * description
  * score
  * topicality
* Safe search annotations
  * adult
  * spoof
  * medical
  * violence
  * racy
* Web detection
  * Web entities
    * entityId - URL
    * score
    * description
  * Full matching images - not really
  * Pages with matching images
    * URL
    * Title
    * Full matching images
  * Visually similar images
  * Best guess labels
    * label
    * language code

[Download](https://owncloud.ut.ee/owncloud/index.php/s/teoFdWKBzzqcFjY)

## DBPedia Spotlight enrichment

Contains the query results after running all of the meme pages' "about" sections through DBPedia Spotlight.

17 MB

38,801 entities

updated 15.05.2021

### Schema

* Input text
* ...
* Resources - the detected entities
  * URI
  * Support
  * Types
  * Surface form
  * Offset
  * Similarity score
  * Percentage of second rank

[Download](https://owncloud.ut.ee/owncloud/index.php/s/iMM8crN4AKSpFZZ)
