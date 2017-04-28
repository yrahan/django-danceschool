# Give this app a custom verbose name to avoid confusion
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .utils.sys import isPreliminaryRun


class CoreAppConfig(AppConfig):
    name = 'danceschool.core'
    verbose_name = _('Core School Functions')

    def ready(self):
        from django.db import connection
        from .constants import getConstant, updateConstant

        # Ensure that signal handlers are loaded
        from . import handlers

        if 'core_emailtemplate' in connection.introspection.table_names() and not isPreliminaryRun():

            EmailTemplate = self.get_model('EmailTemplate')

            success_template_id = getConstant('email__registrationSuccessTemplateID') or 0
            invoice_template_id = getConstant('email__invoiceTemplateID') or 0

            if success_template_id <= 0:
                new_success_template, created = EmailTemplate.objects.get_or_create(
                    name=_('Registration Confirmation Email'),
                    defaults={
                        'subject':_('Registration Confirmation'),
                        'content': '',
                        'defaultCC': '',
                        'hideFromForm': True,}
                )
                # Update constant and fail silently
                updateConstant('email__registrationSuccessTemplateID', new_success_template.id, True)

            if invoice_template_id <= 0:
                new_invoice_template, created = EmailTemplate.objects.get_or_create(
                    name=_('Registration Invoice Email'),
                    defaults={
                        'subject': _('Registration Invoice'),
                        'content': '',
                        'defaultCC': '',
                        'hideFromForm': True,}
                )
                # Update constant and fail silently
                updateConstant('email__invoiceTemplateID',new_invoice_template.id,True)

        if 'core_dancerole' in connection.introspection.table_names() and not isPreliminaryRun():
            DanceRole = self.get_model('DanceRole')

            # Lead and Follow roles are automatically generated, since they are typically used.
            # However, the set of roles for which one can register for any given thing
            # is editable.
            role_lead_id = getConstant('general__roleLeadID') or 0
            role_follow_id = getConstant('general__roleFollowID') or 0

            if role_lead_id <= 0:
                new_lead_role, created = DanceRole.objects.get_or_create(
                    name=_('Lead'),
                    defaults={'order': 1}
                )
                updateConstant('general__roleLeadID',new_lead_role.id,True)
            if role_follow_id <= 0:
                new_follow_role, created = DanceRole.objects.get_or_create(
                    name=_('Follow'),
                    defaults={'order': 2}
                )
                updateConstant('general__roleFollowID',new_follow_role.id,True)

        if 'core_eventstaffcategory' in connection.introspection.table_names() and not isPreliminaryRun():
            EventStaffCategory = self.get_model('EventStaffCategory')

            # Name, preference key, and defaultRate
            new_staff_cats = [
                (_('Class Instruction'),'general__eventStaffCategoryInstructorID',0),
                (_('Assistant Class Instruction'),'general__eventStaffCategoryAssistantID',0),
                (_('Substitute Teaching'),'general__eventStaffCategorySubstituteID',0),
                (_('Other Staff'),'general__eventStaffCategoryOtherID',0),
            ]

            for cat in new_staff_cats:
                if (getConstant(cat[1]) or 0) <= 0:
                    new_cat, created = EventStaffCategory.objects.get_or_create(
                        name=cat[0],
                        defaults={'defaultRate': cat[2]},
                    )
                    # Update constant and fail silently
                    updateConstant(cat[1],new_cat.id,True)