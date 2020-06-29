import UrlResource, HomeResource, GlobalsResource
#
resourceSet = {
    HomeResource.HomeResource : '/',
    GlobalsResource.GlobalsResource : '/config'
}

def addTo(api) :
    for resource, url in resourceSet.items() :
        api.add_resource(resource, resource.url)
