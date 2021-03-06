package main

import (
	"fmt"
	"log"

	"google.golang.org/api/youtube/v3"
)

func printComments(comments []*youtube.CommentThread) {
	for _, item := range comments {
		authorName := item.Snippet.TopLevelComment.Snippet.AuthorDisplayName
		text := item.Snippet.TopLevelComment.Snippet.TextDisplay
		likeCnt := item.Snippet.TopLevelComment.Snippet.LikeCount
		replyCnt := item.Snippet.TotalReplyCount
		fmt.Printf("\"%v\" by %v\nいいね数: %v 返信数: %v\n\n", text, authorName, likeCnt, replyCnt)
	}
}

func getComments(videoID string) []*youtube.CommentThread {
	service := newYoutubeService(newClient())
	call := service.CommentThreads.List("id,snippet").
		VideoId(videoID).
		Order("relevance").
		//SearchTerms("草").
		MaxResults(10)
	response, err := call.Do()
	if err != nil {
		log.Fatalf("%v", err)
	}

	return response.Items
}

func comment(videoID string, message string) {
	service := newYoutubeService(newOAuthClient())
	commentThread := &youtube.CommentThread{
		Snippet: &youtube.CommentThreadSnippet{
			VideoId: videoID,
			TopLevelComment: &youtube.Comment{
				Snippet: &youtube.CommentSnippet{
					TextOriginal: message,
				},
			},
		},
	}
	call := service.CommentThreads.Insert("id,snippet", commentThread)
	_, err := call.Do()
	if err != nil {
		log.Fatalf("%v", err)
	}
	log.Printf("Comment to %v\n", videoID)
}

func reply(commentID string, message string) {
	reply := &youtube.Comment{
		Snippet: &youtube.CommentSnippet{
			ParentId:     commentID,
			TextOriginal: message,
		},
	}
	service := newYoutubeService(newOAuthClient())
	call := service.Comments.Insert("id,snippet", reply)
	_, err := call.Do()
	if err != nil {
		log.Fatalf("%v", err)
	}
	log.Printf("Success\n")
}

func deleteComment(commentID string) {
	service := newYoutubeService(newOAuthClient())
	call := service.Comments.Delete(commentID)
	err := call.Do()
	if err != nil {
		log.Fatalf("%v", err)
	}
	log.Printf("Success\n")
}

// TODO
func deleteAllComment(channelID string, videoID string) {
	// Delete all comment include reply
}
