import mock
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dj_dynamic_settings.models import Setting
from dj_dynamic_settings.registry import registry

User = get_user_model()


class DynamicSettingsViewSetTestCase(APITestCase):
    def setUp(self):
        from dj_dynamic_settings.tests import definitions  # NoQA

        self.base_url = reverse("setting-list")
        user = User.objects.create(is_staff=True, is_superuser=True, is_active=True)
        self.client.force_authenticate(user)
        self.setting_1 = Setting.objects.create(
            key="X_FEATURE_ACTIVE",
            value=True,
            is_active=True,
        )
        self.setting_2 = Setting.objects.create(
            key="X_TRIAL_COUNT",
            value=10,
            is_active=True,
        )

    def test_list(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_list_with_unregistered_setting(self):
        with mock.patch(
            "dj_dynamic_settings.registry.registry.keys", return_value=["X_TRIAL_COUNT"]
        ):
            # Verify that the Setting object still exists after unregistering
            self.assertEqual(Setting.objects.count(), 2)

            response = self.client.get(self.base_url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]["key"], self.setting_2.key)

    def test_retrieve(self):
        url = reverse("setting-detail", kwargs={"pk": self.setting_1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["key"], self.setting_1.key)

    def test_delete(self):
        url = reverse("setting-detail", kwargs={"pk": self.setting_1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Setting.objects.count(), 1)
        self.assertFalse(Setting.objects.filter(pk=self.setting_1.pk).exists())

    def test_update(self):
        url = reverse("setting-detail", kwargs={"pk": self.setting_1.pk})
        response = self.client.patch(url, data={"is_active": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["is_active"], False)
        self.assertEqual(Setting.objects.get(id=self.setting_1.id).is_active, False)

    def test_create(self):
        data = {
            "key": "Y_FEATURE_ACTIVE",
            "value": True,
            "is_active": True,
        }
        response = self.client.post(self.base_url, data=data, format="json")
        setting = Setting.objects.get(key=data["key"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Setting.objects.count(), 3)
        self.assertEqual(setting.key, data["key"])
        self.assertEqual(setting.value, data["value"])

    def test_create_already_exists(self):
        with mock.patch(
            "dj_dynamic_settings.registry.registry.keys", return_value=["X_TRIAL_COUNT"]
        ):
            data = {
                "key": "X_TRIAL_COUNT",
                "value": 100,
            }
            response = self.client.post(self.base_url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                response.json()["key"][0], "setting with this key already exists."
            )

    def test_registry(self):
        url = "{}registry/".format(self.base_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), len(registry.keys()))
