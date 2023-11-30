from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import Timeout as RequestsConnectionTimeoutError
from django.conf import settings
from atlas.models import AtlasDiffObjects
from atlas.models import AtlasForcedPhotometry
from atlas.models import TcsGravityEventAnnotations
from atlas.models import SherlockClassifications
from atlas.models import SherlockCrossmatches
from atlas.models import TcsObjectComments
from atlas.models import TcsCrossMatchesExternal
from django.forms.models import model_to_dict
from .lightcurvequeries import *
from .views import followupClassList

from .views import LC_LIMITS, LC_LIMITS_MD

def candidateddcApi(request, atlas_diff_objects_id):
    """candidateddcApi.

    Args:
        request:
        atlas_diff_objects_id:
    """

    from django.db import connection
    import sys

    # 2021-10-21 KWS Use the Lasair API to do a cone search so we can check for nearby ZTF objects
    from lasair import LasairError, lasair_client as lasair

    transient = AtlasDiffObjects.objects.get(pk=atlas_diff_objects_id)

#    token = settings.LASAIR_TOKEN
#    # 2022-11-16 KWS Added a new timeout parameter, now available from Lasair client
#    #                version v0.0.5+. This should help if Lasair goes offline for any
#    #                reason. But extra (Requests)ConnectionError catch needed.
#    L = lasair(token, endpoint = 'https://lasair-ztf.lsst.ac.uk/api', timeout = 2.0)
#
#    lasairZTFCrossmatches = None
#
#    # If Lasair connectivity problems arise, comment out the following 4 lines.
#    try:
#        lasairZTFCrossmatches = L.cone(transient.ra, transient.dec, 2.0, requestType='all')
#    except RequestsConnectionError as e:
#        # If the API URL is incorrect or times out we will get a connection error.
#        sys.stderr.write('Lasair API Connection Error\n')
#        sys.stderr.write('%s\n' % str(e))
#    except RequestsConnectionTimeoutError as e:
#        # If the API times out, we will get a timeout error.
#        sys.stderr.write('Lasair API Timeout Error\n')
#        sys.stderr.write('%s\n' % str(e))
#    except LasairError as e:
#        sys.stderr.write('Lasair Error\n')
#        sys.stderr.write('%s\n' % str(e))
#        
    # 2017-03-21 KWS Get Gravity Wave annotations and Sherlock Classifications
    sc = SherlockClassifications.objects.filter(transient_object_id_id = transient.id)
    # 2017-11-07 KWS Get Sherlock Crossmatches
    sx = SherlockCrossmatches.objects.filter(transient_object_id_id = transient.id)
    gw = TcsGravityEventAnnotations.objects.filter(transient_object_id_id = transient.id).filter(enclosing_contour__lt=100)
    existingComments = TcsObjectComments.objects.filter(transient_object_id = transient.id).order_by('date_inserted')

    # 2013-10-30 KWS Get external crossmatches if they exist
    externalXMs = TcsCrossMatchesExternal.objects.filter(transient_object_id = transient.id).exclude(matched_list = 'Transient Name Server').order_by('external_designation')

    # 2019-10-18 KWS Get TNS crossmatch if it exists. Yes - another unnecessary hit to the database, but quick.
    tnsXMs = TcsCrossMatchesExternal.objects.filter(transient_object_id = transient.id, matched_list = 'Transient Name Server')

#    # 2014-03-11 KWS Pick up any Finder images.
#    finderImages = TcsPostageStampImages.objects.filter(image_filename__istartswith = str(transient.id), image_type__iendswith = 'finder')
#
    dbName = settings.DATABASES['default']['NAME'].replace('_django', '')

    try:
        detectionLimits = LC_LIMITS[dbName]
    except KeyError as e:
        # Default detections limits for medium deep
        detectionLimits = LC_LIMITS_MD

    lcPoints, lcBlanks, plotLabels, lcLimits = getLCData(transient.id, limits = detectionLimits, conn = connection, ddc = True)

    lc = {'lc': lcPoints,
          'lcNonDets': lcBlanks,
          'plotLabels': plotLabels,
          'lcLimits': lcLimits}

    # 2016-08-11 KWS Get the Forced Photometry data.  We need to completely rethink how this is queried.
    #                In the past I built custom queries that could be called by scripts or web.  Let's
    #                try just building the query using the ORM.

    forcedPhotometry = AtlasForcedPhotometry.objects.filter(atlas_object_id = transient.id).order_by('mjd_obs')

    # 2016-10-16 KWS Just occasionally the forced photometry will NOT produce
    #                a single point on the lightcurve. In this case we should
    #                skip the forced photometry plot.  (In future, we probably
    #                want to plot the non-detections.
    lcForced = {}
    lcDataForced = []
    lcDataForcedFlux = []
    if forcedPhotometry:
        nonLimitingMagsExist = False
        for row in forcedPhotometry:
            if not row.limiting_mag:
                nonLimitingMagsExist = True
                break
        if nonLimitingMagsExist:
            forcedDetectionData, forcedDetectionDataBlanks, forcedPlotLabels, forcedPlotLimits = organiseAtlasForcedPhotometryForPlotting(forcedPhotometry)
            lcDataForced = [forcedDetectionData, forcedDetectionDataBlanks, forcedPlotLabels, forcedPlotLimits]
            forcedDetectionData, forcedDetectionDataBlanks, forcedPlotLabels, forcedPlotLimits = organiseAtlasForcedFluxPhotometryForPlotting(forcedPhotometry)
            lcDataForcedFlux = [forcedDetectionData, forcedDetectionDataBlanks, forcedPlotLabels, forcedPlotLimits]



#    forcedDiffStackPhotometry = AtlasStackedForcedPhotometry.objects.filter(atlas_object_id = transient.id).filter(ujy__lt = 10000).filter(ujy__gt = -10000).exclude(ujy = 0, dujy = 999).order_by('mjd')
#    lcDataForcedStackFlux = []
#
#    if forcedDiffStackPhotometry:
#        forcedStackDetectionData, forcedStackDetectionDataBlanks, forcedStackPlotLabels, forcedStackPlotLimits = organiseAtlasForcedFluxPhotometryForPlottingJT(forcedDiffStackPhotometry)
#        lcDataForcedStackFlux = [forcedStackDetectionData, forcedStackDetectionDataBlanks, forcedStackPlotLabels, forcedStackPlotLimits]
#
#    # Get the recurrence data. With the ATLAS schema, we already have all the detections in one place.
#    # Note that we should probably aggregate this code together into a function.
#
#    detections = AtlasDetectionsddc.objects.filter(atlas_object_id = transient.id).filter(deprecated__isnull = True)
#
#    # Convert the detections to a format understandable by the rms calculator.
#    recurrences = []
#    footprints = []
#    for row in detections:
#        # 2019-11-02 KWS Exclude all negative detections in average RA/Dec calculation.
#        if row.det != 5:
#            recurrences.append({"RA": row.ra, "DEC": row.dec})
#        footprints.append({"RA": row.atlas_metadata_id.ra, "DEC": row.atlas_metadata_id.dec, "footprintName": row.atlas_metadata_id.obj})
#
#    # 2019-11-02 KWS Redo the recurrences if there are NO positive recurrences.
#    if len(recurrences) == 0:
#        recurrences = []
#        for row in detections:
#            recurrences.append({"RA": row.ra, "DEC": row.dec})
#
#    distinctFootprints = set([f['footprintName'] for f in footprints])
#
#    fpData = {}
#
#    if len(distinctFootprints) == 1:
#        # We have exactly one footprint
#        # Use the average RA and Dec as the input RA and Dec (where the origin will be plotted)
#        # (Yes - I know - we are doing this calculation twice!)
#        avgRa, avgDec, rms = calculateRMSScatter(footprints)
#        fprecurrencePlotData, fprecurrencePlotLabels, fpaverageObjectCoords, fprmsScatter = getRecurrenceDataForPlotting(footprints, avgRa, avgDec, objectColour = 21)
#        fpData['plotdata'] = fprecurrencePlotData
#        fpData['plotlabels'] = fprecurrencePlotLabels
#        fpData['avgcoords'] = fpaverageObjectCoords
#        fpData['rms'] = fprmsScatter
#
#
#    recurrencePlotData, recurrencePlotLabels, averageObjectCoords, rmsScatter = getRecurrenceDataForPlotting(recurrences, transient.ra, transient.dec, objectColour = 20)
#    avgCoords = {'ra': averageObjectCoords[0]["RA"], 'dec': averageObjectCoords[0]["DEC"], 'ra_sex': ra_to_sex(averageObjectCoords[0]["RA"]), 'dec_sex': dec_to_sex(averageObjectCoords[0]["DEC"]), 'ra_in_hours': ra_in_decimal_hours(averageObjectCoords[0]["RA"])}
#
#    galactic = transform([averageObjectCoords[0]["RA"], averageObjectCoords[0]["DEC"]], J2000toGalactic)
#
#    # Lightcurve data
#    lcData = [lcPoints, lcBlanks, plotLabels]
#
#    detectionList = transient.detection_list_id
#
#    userListQuerySet = TcsObjectGroups.objects.filter(transient_object_id = transient.id)
#
#    # Grab all the lists of which this object is a member, so that we can exclude these from
#    # the user lists to which we want to add this object.
#    userListIds = []
#    for row in userListQuerySet:
#        userListIds.append(row.object_group_id)
#
#    listId = None
#    if detectionList:
#        listId = detectionList.id
#
#    import sys
#
#    coneSearchRadius = 8.0   # arcsec
#
#    xmObjects = None
#
#    # Grab all objects within 3 arcsec of this one.
#    xmList = []
#    catalogueName = 'atlas_diff_objects'
#    message, xmObjects = coneSearchHTM(transient.ra, transient.dec, coneSearchRadius, catalogueName, queryType = FULL, conn = connection, django = True)
#
#    if xmObjects:
#        numberOfMatches = len(xmObjects)
#        # Add the objects into a list of dicts that have consistent names for all catalogues
#
#        for xm in xmObjects:
#            sys.stderr.write("\n%s\n" % str(xm))
#            # Add to the list all object ids except the current one (which will have
#            # a separation of zero).
#            if xm[1][CAT_ID_RA_DEC_COLS[catalogueName][0][0]] != transient.id:
#                xmList.append({'xmseparation': xm[0], 'xmid': xm[1][CAT_ID_RA_DEC_COLS[catalogueName][0][0]]})
#                xmid = xm[1][CAT_ID_RA_DEC_COLS[catalogueName][0][0]]
#                xmra = xm[1][CAT_ID_RA_DEC_COLS[catalogueName][0][1]]
#                xmdec = xm[1][CAT_ID_RA_DEC_COLS[catalogueName][0][2]]
#                xmName = xm[1]["atlas_designation"]
#                if not xmName:
#                    xmName = xmid
#
#                xmDetections = AtlasDetectionsddc.objects.filter(atlas_object_id = xmid)
#                xmRecurrences = []
#                # 2019-11-02 KWS Only add the crossmatch recurrences if they are positive.
#                for xmDet in xmDetections:
#                    if xmDet.det != 5:
#                        xmRecurrences.append({"RA": xmDet.ra, "DEC": xmDet.dec})
#
#                if len(xmRecurrences) == 0:
#                    xmRecurrences = []
#                    for xmDet in xmDetections:
#                        xmRecurrences.append({"RA": xmDet.ra, "DEC": xmDet.dec})
#
#                xmrecurrencePlotData, xmrecurrencePlotLabels, xmaverageObjectCoords, xmrmsScatter = getRecurrenceDataForPlotting(xmRecurrences, transient.ra, transient.dec, secRA = xmra, secDEC = xmdec, secId = xmid, secName = xmName, objectColour = 23)
#                recurrencePlotData += xmrecurrencePlotData
#                recurrencePlotLabels += xmrecurrencePlotLabels
#                averageObjectCoords += xmaverageObjectCoords
#                rmsScatter += xmrmsScatter
#
#    recurrenceData = [recurrencePlotData, recurrencePlotLabels, averageObjectCoords, rmsScatter]
#
#    data = {}
#
#    return render(request, 'atlas/' + template_name,{'transient' : transient, 'table': table, 'images': transient_images, 'form' : form, 'avg_coords': avgCoords, 'lcdata': lcData, 'lcdataforced': lcDataForced, 'lcdataforcedflux': lcDataForcedFlux, 'lcdataforcedstackflux': lcDataForcedStackFlux, 'lclimits': lcLimits, 'recurrencedata': recurrenceData, 'conesearchold': xmresults['oldDBXmList'], 'olddburl': xmresults['oldDBURL'], 'externalXMs': externalXMs, 'tnsXMs': tnsXMs, 'public': public, 'form_searchobject': formSearchObject, 'dbName': dbName, 'finderImages': finderImages, 'processingStatus': processingStatus, 'galactic': galactic, 'fpData': fpData, 'sc': sc, 'gw': gw, 'comments': existingComments, 'sx': sx, 'lasairZTFCrossmatches': lasairZTFCrossmatches})
#
#            'sclass': model_to_dict(sc),
#            'scross': model_to_dict(sx),
#            'gw': model_to_dict(gw),
    data = {'object': model_to_dict(transient),
            'lc': lc,
            'sherlock_crossmatches': [model_to_dict(s) for s in sx],
            'tns_crossmatches': [model_to_dict(t) for t in tnsXMs],
            'external_crossmatches': [model_to_dict(e) for e in externalXMs]}

    return data


def getObjectList(request, listId):
    querySet = followupClassList[int(listId)].objects.all()
    objectList = []

    for row in querySet:
        objectList.append(model_to_dict(row))

    return objectList
