from . import base
from diabolocom_api_client.utils import urljoin

class CampaignsV2ContactsPool(
    base.ResourcePool,
    base.GettableResource,
    base.CreatableResource,
    base.UpdatableResource,
    base.DeletableResource
):
    
    @property
    def search(self):
        return base.ActionPool(
            urljoin(self._endpoint, 'search'), self._session
        )
    
class CampaignsV2ContactBatchStatusPool(
    base.ResourcePool,
    base.GettableResource
):
    pass

class CampaignsV2ContactBatchPool(
    base.ResourcePool
):    
    @property
    def create(self):
        return base.ActionPool(
            urljoin(self._endpoint, 'create'), self._session
        )

    @property
    def update(self):
        return base.ActionPool(
            urljoin(self._endpoint, 'update'), self._session
        )

    @property
    def delete(self):
        return base.ActionPool(
            urljoin(self._endpoint, 'delete'), self._session
        )

    @property
    def status(self):
        return CampaignsV2ContactBatchStatusPool(
            urljoin(self._endpoint, 'status'), self._session
        )

class CampaignsV2Pool(
    base.ResourcePool
):
    def contacts(self, campaign_id):
        return CampaignsV2ContactsPool(
            urljoin(self._endpoint, campaign_id, 'contacts'), self._session
        )

    def contact_batch(self, campaign_id):
        return CampaignsV2ContactBatchPool(
            urljoin(self._endpoint, campaign_id, 'contact-batch'), self._session
        )


class CampaignsPool(
    base.ResourcePool,
    base.ListableResource,
    base.GettableResource,
    base.DeletableResource
):

    def field(self, campaign_id):
        return base.ActionPool(
            urljoin(self._endpoint, campaign_id, 'field'), self._session
        )