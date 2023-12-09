# Movie scraper
Movie scraper is a tool for extracting information about currently available movies on popular streaming services. The aim of the project is to create an up-to-date, local database containing information such as:

 - Title
 - Year of production
 - Link to streaming service
 - Link to thumbnail
 - Final date of material availability
 
**Works with Jellyfin, Emby, Plex**  
The software can also export movies and series in a format recognized by popular Free Software Media Systems like Jellyfin, Emby or Plex, organizing all the media available to you in one place. Example:  

<p align="center">
  <img width="500" height="500" src="https://github.com/Crudelis98/Movie-scraper/blob/main/images/jellyfin_dashboard_netflix_movies.PNG">
</p>

*Movies*  
├── Film (1990).mp4  
├── Film (1994).mp4  
├── Film (2008)  
│   └── Film.mkv  
└── Film (2010)  
    ├── Film-cd1.avi  
    └── Film-cd2.avi  

*Shows*  
├── Series (2010)  
│   ├── Season 00  
│   │   ├── Some Special.mkv  
│   │   ├── Episode S00E01.mkv  
│   │   └── Episode S00E02.mkv  
│   ├── Season 01  
│   │   ├── Episode S01E01-E02.mkv  
│   │   ├── Episode S01E03.mkv  
│   │   └── Episode S01E04.mkv  
│   └── Season 02  
│       ├── Episode S02E01.mkv  
│       ├── Episode S02E02.mkv  
│       ├── Episode S02E03 Part 1.mkv  
│       └── Episode S02E03 Part 2.mkv  
└── Series (2018)  
    ├── Episode S01E01.mkv  
    ├── Episode S01E02.mkv  
    ├── Episode S02E01-E02.mkv  
    └── Episode S02E03.mkv  

**Currently supported platforms:**  
	 - Windows 10/11  
  
**Currently supported browsers:**  
	- Google chrome  
 
**Currently supported streaming services:**  
	 - Netflix  
  
**Planned support for:**  
	- Microsoft Edge  
	- Firefox  
 	- Opera  
	- Disney  
	- HBO  
	- Prime Video  
 
**FAQ**  
*Can I watch movies outside of streaming platform?*  
No, but I am developing unified media player that gives somewhat native experince of watching movies inside Jellyfin. Feel free to sponsor this project if you are intrested.  

*Can I download movies?*  
No.  
