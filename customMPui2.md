
Evolveum midPoint Chatbot (beta)

This chatbot uses publicly available information from Evolveum. Responses may be inaccurate or biased; human oversight is recommended. Evolveum is not liable for any resulting actions or damages.

Do not enter private or sensitive information. By using this chatbot, you agree that your input and responses ("Content") may be used by Evolveum to improve services.

The timeout for the chatbot is set to 12 minutes, so if you experience a timeout, you can try to rephrase your question (if there was an error related to repetition) or wait for a while and try again in case the chatbot is overloaded.

Feedback is encouraged to enhance the chatbot's effectiveness and will be reviewed by Evolveum. If you did not get the right answer, you can still use traditional communication methods like the mailing list, support portal, and documentation.

Due to the beta nature of this chatbot, it is available only on weekdays from 7:00 to 21:00 CE(S)T.

_customize the ui by adding a screen that will show the logged in user all the resources to which they have access_

To customize the midPoint UI to show the logged-in user all the resources to which they have access, you can leverage the Customizable Dashboards feature. This allows you to create a custom dashboard that displays relevant information based on the user's access rights.

Here is a step-by-step guide to achieve this:

    Create a Custom Dashboard:
        Navigate to the System Configuration.
        Go to the Admin GUI Configuration section.
        Add a new Custom Dashboard.

    Define the Dashboard Content:
        Use the midPoint Query Language (MQL) to define the resources to which the user has access.
        The query should filter resources based on the user's assignments or roles.

    Add a Widget to Display Resources:
        Add a widget to the dashboard that will display the list of resources.
        Configure the widget to use the MQL query defined in the previous step.

Here is an example of the MQL query to find resources to which the user has access:

assignment/targetRef matches (targetType = ResourceType)

This query will return all resources that are assigned to the user directly or indirectly through roles.

    Configure the Widget:
        Set the widget to display the results of the query.
        Customize the widget to show relevant information such as the resource name, type, and status.

    Test the Dashboard:
        Log in as a user and navigate to the custom dashboard.
        Verify that the dashboard displays the correct resources based on the user's access rights.

By following these steps, you can create a custom dashboard in midPoint that shows the logged-in user all the resources to which they have access.

Resources:

    https://docs.evolveum.com/midpoint/guides/admin-gui-user-guide/
    https://docs.evolveum.com/midpoint/reference/master/interfaces/rest/operations/examples/search-objects-filter/
    https://support.evolveum.com/work_packages/8766

add detailed instructions to each of the steps you listed

AI Output Step Reasoning

Step 1: Create a Custom Dashboard

Access System Configuration:

    Log in to midPoint as an administrator.
    Navigate to Configuration > System.
    Click on Admin GUI Configuration.

Add a New Dashboard:

    In the User Dashboards tab, click Add.
    Define the dashboard configuration:

    <configurableUserDashboard>
        <identifier>user-resources-dashboard</identifier>
        <configurableDashboardRef oid="12345678-1234-1234-1234-1234567890ab" type="c:DashboardType"/>
        <visibility>visible</visibility>
    </configurableUserDashboard>

        Replace oid with the actual OID of the dashboard you will create in Step 2.

Step 2: Define the Dashboard and Widget

Create the Dashboard Object:

    Navigate to Objects > Dashboards.
    Click New Dashboard and define it:

    <dashboard oid="12345678-1234-1234-1234-1234567890ab">
        <name>User Resources Dashboard</name>
        <display>
            <label>User Resources</label>
        </display>
        <widget>
            <identifier>user-resources</identifier>
            <display>
                <label>Resources I Have Access To</label>
                <color>#00a65a</color>
                <icon>
                    <cssClass>fa fa-server</cssClass>
                </icon>
            </display>
            <data>
                <sourceType>objectCollection</sourceType>
                <collection>
                    <collectionRef oid="87654321-4321-4321-4321-ba0987654321" type="ObjectCollectionType"/>
                </collection>
            </data>
        </widget>
    </dashboard>

    Replace collectionRef with the OID of the object collection created in Step 3.

Create an Object Collection:

    Navigate to Objects > Object Collections.
    Click New Object Collection and define it:

    <objectCollection oid="87654321-4321-4321-4321-ba0987654321">
        <name>User Access Resources</name>
        <type>ResourceType</type>
        <filter>
            <q:in>
                <q:expression>
                    <q:assignment>
                        <q:targetRef>
                            <q:type>ResourceType</q:type>
                        </q:targetRef>
                    </q:assignment>
                </q:expression>
                <q:collection>
                    <q:collectionRef oid="user-assignments-collection" type="ObjectCollectionType"/>
                </q:collection>
            </q:in>
        </filter>
    </objectCollection>

        This query filters resources based on the user's assignments.

Step 3: Configure the MQL Query

Define the MQL Query:

    The query should identify resources assigned to the user. Example:

    assignment/targetRef matches (targetType = ResourceType)

This query retrieves all resources directly assigned to the user. For indirect access via roles, use:

assignment/indirectTargetRef matches (targetType = ResourceType)

    Link the Query to the Object Collection:
        Ensure the object collection (created in Step 2) uses the MQL query to filter resources.

Step 4: Test the Dashboard

    Log in as a Test User:
        Log in as a user with specific resource assignments.
        Navigate to Dashboards > User Resources Dashboard.
        Verify the widget displays the correct resources.

    Troubleshoot if Necessary:
        If the widget shows no data, check:
            The MQL query syntax.
            The object collection's collectionRef is correctly linked.
            The user has assignments or roles granting access to resources.

Optional: Schedule a Report for Asynchronous Widgets
Create a Report Task:

    Navigate to Objects > Reports.
    Define a report to update the widget data asynchronously:

    <report>
        <name>User Resources Report</name>
        <dashboard>
            <dashboardRef oid="12345678-1234-1234-1234-1234567890ab"/>
            <storeExportedWidgetData>onlyWidget</storeExportedWidgetData>
        </dashboard>
    </report>

        Schedule the report to run periodically (e.g., daily) to keep the widget data up-to-date.

Final Notes

    Permissions: Ensure the dashboard is visible to end users by configuring visibility in configurableUserDashboard.
    Customization: Adjust widget colors, icons, and labels to match your organization's branding.
    Testing: Validate the setup with users having different access levels to ensure accuracy.

Resources:

    https://docs.evolveum.com/midpoint/reference/master/misc/reports/configuration/dashboard-report/
    https://lists.evolveum.com/pipermail/midpoint/2023-April/007691.html
    https://docs.evolveum.com/midpoint/reference/master/admin-gui/dashboards/configuration/

non-commercial use only
