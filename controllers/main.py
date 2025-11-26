# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from markupsafe import Markup


class SchoolTransportController(http.Controller):
    
    @http.route('/school_transport/map/<int:route_id>', type='http', auth='user', website=True)
    def transport_map(self, route_id, **kwargs):
        """Render the interactive map for a transport route."""
        route = request.env['school.transport.route'].browse(route_id)
        
        if not route.exists():
            return request.render('at_school_management.transport_map_error', {
                'error': 'Route not found'
            })
        
        # Get map data
        map_data = route.get_map_data()
        
        return request.render('at_school_management.transport_map_template', {
            'route': route,
            'map_data': Markup(json.dumps(map_data)),
            'center_lat': route.map_center_lat or 16.0544,
            'center_lon': route.map_center_lon or 108.2022,
        })
    
    @http.route('/school_transport/api/route/<int:route_id>', type='json', auth='user')
    def get_route_data(self, route_id, **kwargs):
        """API endpoint to get route data as JSON."""
        route = request.env['school.transport.route'].browse(route_id)
        
        if not route.exists():
            return {'error': 'Route not found'}
        
        return route.get_map_data()
