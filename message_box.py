from odoo import api, fields, models, _

MESSAGE_TYPES = [('warning','Warning'),('info','Information'),('error','Error')]

class MessageBox(models.TransientModel):
	_name = 'message_box'
	_description = 'Show message box to user'
	m_type = fields.Selection(MESSAGE_TYPES, string='Type', readonly=True)
	m_title = fields.Char(string="Title", size=100, readonly=True)
	m_text = fields.Text(string="Message", readonly=True)

	@api.multi
	def _get_view_id(self):
		"""Get the view id
			@return: view id, or False if no view found
		"""
		res = self.env['ir.model.data'].get_object_reference('message_box', 'message_box_form')
		return res and res[1] or False

	@api.multi
	def message(self, m_title, m_text, m_type, context):
		message = self.create({'m_title': m_title, 'm_text': m_text, 'm_type': m_type})
		message_type = [t[1]for t in MESSAGE_TYPES if m_type == t[0]][0]
		#print '%s: %s' % (_(message_type), _(m_title))
		return {
			'name': '%s: %s' % (_(message_type), _(m_title)),
			'view_type': 'form',
			'view_mode': 'form',
			'view_id': self._get_view_id(),
			'res_model': 'message_box',
			'domain': [],
			'context': context,
			'type': 'ir.actions.act_window',
			'target': 'new',
			'res_id': message.id
		}

	@api.multi
	def warning(self, title, text, context=None):
		return self.message(m_title=title, m_text=text, m_type='warning', context=context)

	@api.multi
	def info(self, title, text, context=None):
		return self.message(m_title=title, m_text=text, m_type='info', context=context)

	@api.multi
	def error(self, title, text, context=None):
		return self.message(m_title=title, m_text=text, m_type='error', context=context)
