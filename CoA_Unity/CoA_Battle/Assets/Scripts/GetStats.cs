﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Text;
using System.IO;  

using UnityEngine.Networking;

//Get the player's stats from the database
public class GetStats : MonoBehaviour {
	Text showStats;
	UnityWebRequest webRequest;
	AsyncOperation requestOp;

	// Use this for initialization
	void Start () {
		showStats = GetComponent<Text> (); //Debug print the stats from database
		//This is the controller function that returns all the stats
		webRequest = new UnityWebRequest ("http://127.0.0.1:8000/callofadventure/battle/web2unity");
		webRequest.downloadHandler = new DownloadHandlerBuffer (); //Handles reading in text from database
		requestOp = webRequest.Send (); //Starts communications with database (sends the request)
	}

	// Update is called once per frame
	void Update () {
		if (requestOp.isDone) { //Check if done reading in input
			showStats.text = webRequest.downloadHandler.text; //Get text data
			Parse(showStats.text);
		} else {
			showStats.text = "Getting data from database...";
		}
	}

	// Tokenize and parse data string
	string[] Parse (string data) {
		char[] delim = { '%' };
		string[] stat_arr = data.Split (delim);
		print ("location: " + stat_arr[0]);
		print ("name: " + stat_arr[1] + " " + stat_arr[2]);
		print ("attack: " + stat_arr[3]);
		print ("defense: " + stat_arr[4]);
		return stat_arr;
	}
}	