import UrlResource, HomeResource, GlobalsResource

resourceSet = {
    HomeResource.HomeResource : UrlResource.HOME,
    GlobalsResource.GlobalsResource : UrlResource.GLOBALS
}

def addTo(api) :
    for resource, url in resourceSet.items() :
        api.add_resource(resource, resource.url)
