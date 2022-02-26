---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: post
author_profile: true
title: TEST
---

site.posts : {{site.posts}}
My Posts:
<ul>
	{% for post in site.posts %}
	<li>
		<a href="{{post.url}}">{{post.title}}</a>
		{{post.excerpt}}
	</li>
	{% endfor %}
</ul>
