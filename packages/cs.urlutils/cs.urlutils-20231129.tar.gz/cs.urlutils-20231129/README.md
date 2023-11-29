URL related utility functions and classes.
- Cameron Simpson <cs@cskk.id.au> 26dec2011
#

*Latest release 20231129*:
* Drop Python 2 support.
* No longer use cs.xml, which is going away.
* Make _URL type public as URL with a new promote() method, drop URL factory function, update URL constructors throughout.
* URL.__init__: make parameters keyword only.

## Class `NetrcHTTPPasswordMgr(urllib.request.HTTPPasswordMgrWithDefaultRealm, urllib.request.HTTPPasswordMgr)`

A subclass of `HTTPPasswordMgrWithDefaultRealm` that consults
the `.netrc` file if no overriding credentials have been stored.

## Function `skip_errs(iterable)`

Iterate over `iterable` and yield its values.
If it raises URLError or HTTPError, report the error and skip the result.

## Function `strip_whitespace(s)`

Strip whitespace characters from a string, per HTML 4.01 section 1.6 and appendix E.

## Class `URL(builtins.str, cs.deco.Promotable)`

Utility class to do simple stuff to URLs, subclasses `str`.

*Method `URL.GET(self)`*:
Fetch the URL content.
If there is an HTTPError, report the error, flush the
content, set self._fetch_exception.
This means that that accessing the self.content property
will always attempt a fetch, but return None on error.

*Method `URL.__getattr__(self, attr)`*:
Ad hoc attributes.
Upper case attributes named "FOO" parse the text and find the (sole) node named "foo".
Upper case attributes named "FOOs" parse the text and find all the nodes named "foo".

*Property `URL.content`*:
The URL content as a string.

*Property `URL.content_length`*:
The value of the Content-Length: header or None.

*Property `URL.content_transfer_encoding`*:
The URL content tranfer encoding.

*Property `URL.content_type`*:
The URL content MIME type.

*Method `URL.default_limit(self)`*:
Default URLLimit for this URL: same host:port, any subpath.

*Property `URL.domain`*:
The URL domain - the hostname with the first dotted component removed.

*Method `URL.exists(self)`*:
Test if this URL exists, return Boolean.

*Method `URL.feedparsed(self)`*:
A parse of the content via the feedparser module.

*Method `URL.find_all(self, *a, **kw)`*:
Convenience routine to call BeautifulSoup's .find_all() method.

*Method `URL.flush(self)`*:
Forget all cached content.

*Property `URL.fragment`*:
The URL fragment as returned by urlparse.urlparse.

*Method `URL.get_content(self, onerror=None)`*:
Probe URL for content to avoid exceptions later.
Use, and save as .content, `onerror` in the case of HTTPError.

*Property `URL.hostname`*:
The URL hostname as returned by urlparse.urlparse.

*Method `URL.hrefs(self, absolute=False)`*:
All 'href=' values from the content HTML 'A' tags.
If `absolute`, resolve the sources with respect to our URL.

*Property `URL.last_modified`*:
The value of the Last-Modified: header as a UNIX timestamp, or None.

*Property `URL.netloc`*:
The URL netloc as returned by urlparse.urlparse.

*Method `URL.normalised(self)`*:
Return a normalised URL where "." and ".." components have been processed.

*Property `URL.params`*:
The URL params as returned by urlparse.urlparse.

*Property `URL.parsed`*:
The URL content parsed as HTML by BeautifulSoup.

*Property `URL.parts`*:
The URL parsed into parts by urlparse.urlparse.

*Property `URL.password`*:
The URL password as returned by urlparse.urlparse.

*Property `URL.path`*:
The URL path as returned by urlparse.urlparse.

*Property `URL.path_elements`*:
Return the non-empty path components; NB: a new list every time.

*Property `URL.port`*:
The URL port as returned by urlparse.urlparse.

*Method `URL.promote(obj)`*:
Promote `obj` to an instance of `cls`.
Instances of `cls` are passed through unchanged.
`str` if promoted to `cls(obj)`.
`(url,referer)` is promoted to `cls(url,referer=referer)`.

*Property `URL.query`*:
The URL query as returned by urlparse.urlparse.

*Method `URL.resolve(self, base)`*:
Resolve this URL with respect to a base URL.

*Method `URL.savepath(self, rootdir)`*:
Compute a local filesystem save pathname for this URL.
This scheme is designed to accomodate the fact that 'a',
'a/' and 'a/b' can all coexist.
Extend any component ending in '.' with another '.'.
Extend directory components with '.d.'.

*Property `URL.scheme`*:
The URL scheme as returned by urlparse.urlparse.

*Method `URL.srcs(self, *a, **kw)`*:
All 'src=' values from the content HTML.
If `absolute`, resolve the sources with respect to our URL.

*Method `URL.unsavepath(savepath)`*:
Compute URL path component from a savepath as returned by URL.savepath.
This should always round trip with URL.savepath.

*Property `URL.username`*:
The URL username as returned by urlparse.urlparse.

*Method `URL.walk(self, limit=None, seen=None, follow_redirects=False)`*:
Walk a website from this URL yielding this and all descendent URLs.
`limit`: an object with a contraint test method "ok".
         If not supplied, limit URLs to the same host and port.
`seen`: a setlike object with a "__contains__" method and an "add" method.
         URLs already in the set will not be yielded or visited.
`follow_redirects`: whether to follow URL redirects

*Property `URL.xml`*:
An `ElementTree` of the URL content.

*Method `URL.xml_find_all(self, match)`*:
Convenience routine to call ElementTree.XML's .findall() method.

# Release Log



*Release 20231129*:
* Drop Python 2 support.
* No longer use cs.xml, which is going away.
* Make _URL type public as URL with a new promote() method, drop URL factory function, update URL constructors throughout.
* URL.__init__: make parameters keyword only.

*Release 20191004*:
Small updates for changes to other modules.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20160827*:
* Handle TimeoutError, reporting elapsed time.
* URL: present ._fetch as .GET.
* URL: add .resolve to resolve this URL against a base URL.
* URL: add .savepath and .unsavepath methods to generate nonconflicting save pathnames for URLs and the reverse.
* URL._fetch: record the post-redirection URL as final_url.
* New URLLimit class for specifying simple tests for URL acceptance.
* New walk(): method to walk website from starting URL, yielding URLs.
* URL.content_length property, returns int or None if header missing.
* New URL.normalised method to return URL with . and .. processed in the path.
* new URL.exists test function.
* Assorted bugfixes and improvements.

*Release 20150116*:
Initial PyPI release.
