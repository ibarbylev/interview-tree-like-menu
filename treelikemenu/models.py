from django.db import models
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('menu name'))
    slug = models.SlugField(max_length=100, verbose_name=_('menu name for url'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name=_('menu name'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('submenu'))
    name = models.CharField(max_length=100, verbose_name=_('menu item name'))
    slug = models.SlugField(max_length=100, verbose_name=_('menu item name for url'))

    class Meta:
        ordering = ['pk']
        verbose_name = _('MenuItem')
        verbose_name_plural = _('MenuItems')

    def __str__(self):
        return f'{self.name} - {self.menu} - {self.parent}'
