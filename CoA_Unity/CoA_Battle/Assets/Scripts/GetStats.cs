using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Text;
using System.IO;  

using UnityEngine.Networking;

public class GetStats : MonoBehaviour {
	Text showStats;
	UnityWebRequest webRequest;
	AsyncOperation requestOp;

	// Use this for initialization
	void Start () {
		showStats = GetComponent<Text> ();
		webRequest = new UnityWebRequest ("http://127.0.0.1:8000/callofadventure/default/unitywrtest");
		webRequest.downloadHandler = new DownloadHandlerBuffer ();
		requestOp = webRequest.Send ();
	}

	// Update is called once per frame
	void Update () {
		if (requestOp.isDone) {
			showStats.text = webRequest.downloadHandler.text; 
		}
	}
}
