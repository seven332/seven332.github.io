Title: SwitchPreference 在 pre-L 下的 bug
Date: 2015-9-29 16:15
Category: Android

在 [Nimingban](https://github.com/seven332/Nimingban) 这个应用中，最开始我是把暗色主题用 SwitchPreference 放在设置界面里的，而且是第一项。后来有用户反馈说是把设置往下滑动，会出现界面闪烁。我听后感觉很奇怪，因为我这不能重现这个 bug，而且设置界面这方面的代码我也没有用什么奇技淫巧，想必不太可能是我的锅。既然不是我的锅那么就是系统的锅了。好在这个问题貌似只是几个用户会遇到，我也就没太注意，直接在设置中删掉暗色主题的设置，移到右侧栏的下面，自认为完美地解决了这个问题。

后来又看到有用户反馈说随着设置界面的滑动，设置项的值会变化。看来这个问题并没有被解决。想想看肯定还是系统的问题。查询了一番果然是系统的问题，而且 lollipop 以下的都有这个问题。这个问题已经有人在 stackoverflow 上[问了](http://stackoverflow.com/questions/15632215/preference-items-being-automatically-re-set)，而且提交了 [issue](https://code.google.com/p/android/issues/detail?id=26194)。

问题的原因在提交的 issue 里描述的很清楚。PreferenceFragment 用的是 ListView，ListView 会对控件重复使用，问题就出现在重复使用的过程中。

kitkat-mr2.2-release (API 19) SwitchPreference 相关片段

    :::java
    private final Listener mListener = new Listener();

    private class Listener implements CompoundButton.OnCheckedChangeListener {
        @Override
        public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
            if (!callChangeListener(isChecked)) {
                // Listener didn't like it, change it back.
                // CompoundButton will make sure we don't recurse.
                buttonView.setChecked(!isChecked);
                return;
            }

            SwitchPreference.this.setChecked(isChecked);
        }
    }
	
    @Override
    protected void onBindView(View view) {
        super.onBindView(view);

        View checkableView = view.findViewById(com.android.internal.R.id.switchWidget);
        if (checkableView != null && checkableView instanceof Checkable) {
            ((Checkable) checkableView).setChecked(mChecked);

            sendAccessibilityEvent(checkableView);

            if (checkableView instanceof Switch) {
                final Switch switchView = (Switch) checkableView;
                switchView.setTextOn(mSwitchOn);
                switchView.setTextOff(mSwitchOff);
                switchView.setOnCheckedChangeListener(mListener);
            }
        }

        syncSummaryView(view);
    }

lollipop-release (API 21) SwitchPreference 相关片段

    :::java
    private final Listener mListener = new Listener();

    private class Listener implements CompoundButton.OnCheckedChangeListener {
        @Override
        public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
            if (!callChangeListener(isChecked)) {
                // Listener didn't like it, change it back.
                // CompoundButton will make sure we don't recurse.
                buttonView.setChecked(!isChecked);
                return;
            }

            SwitchPreference.this.setChecked(isChecked);
        }
    }
	
    @Override
    protected void onBindView(View view) {
        super.onBindView(view);

        View checkableView = view.findViewById(com.android.internal.R.id.switchWidget);
        if (checkableView != null && checkableView instanceof Checkable) {
            if (checkableView instanceof Switch) {
                final Switch switchView = (Switch) checkableView;
                switchView.setOnCheckedChangeListener(null);
            }

            ((Checkable) checkableView).setChecked(mChecked);

            if (checkableView instanceof Switch) {
                final Switch switchView = (Switch) checkableView;
                switchView.setTextOn(mSwitchOn);
                switchView.setTextOff(mSwitchOff);
                switchView.setOnCheckedChangeListener(mListener);
            }
        }

        syncSummaryView(view);
    }

在 onBindView 里可以看到明显的不同，在 lollipop-release 中多了 switchView.setOnCheckedChangeListener(null)，这就是用来解决这个 bug 的。

假设在滚动 ListView 的过程中，上面的 SwitchPreference 滑出了屏幕，下面的 SwitchPreference 滑入了屏幕，那么下面的 SwitchPreference 就会用上面的 SwitchPreference 的控件，下面的 SwitchPreference 的 onBindView 中的 checkableView 就会是上面的 SwitchPreference 的 Switch。这个时候在 kitkat-mr2.2-release 中，会直接 setChecked，倘若两个 SwitchPreference 的值不同，就会引起 Switch 的 OnCheckedChangeListener 调用 onCheckedChanged。但是此时，Switch 的 OnCheckedChangeListener 依旧是上面的 SwitchPreference 的 mListener 字段，这就导致上面的 SwitchPreference 的值的变化，产生了 bug。

解决方法也是直接在 setChecked 之前设置 OnCheckedChangeListener 为 null。

当然我无法修改用户手机系统，只好自己重写。

FixedSwitchPreference.java

```java
public class FixedSwitchPreference extends TwoStatePreference {

    private static Method sSyncSummaryViewMethod;

    static {
        try {
            sSyncSummaryViewMethod = TwoStatePreference.class.getDeclaredMethod("syncSummaryView", View.class);
            sSyncSummaryViewMethod.setAccessible(true);
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
            sSyncSummaryViewMethod = null;
        }
    }

    // Switch text for on and off states
    private CharSequence mSwitchOn;
    private CharSequence mSwitchOff;

    private final Listener mListener = new Listener();

    private class Listener implements CompoundButton.OnCheckedChangeListener {
        @Override
        public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
            if (!callChangeListener(isChecked)) {
                // Listener didn't like it, change it back.
                // CompoundButton will make sure we don't recurse.
                buttonView.setChecked(!isChecked);
                return;
            }

            FixedSwitchPreference.this.setChecked(isChecked);
        }
    }

    public FixedSwitchPreference(Context context) {
        super(context);
        init(context, null, 0, 0);
    }

    public FixedSwitchPreference(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(context, attrs, 0, 0);
    }

    public FixedSwitchPreference(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init(context, attrs, defStyleAttr, 0);
    }

    @TargetApi(Build.VERSION_CODES.LOLLIPOP)
    public FixedSwitchPreference(Context context, AttributeSet attrs, int defStyleAttr, int defStyleRes) {
        super(context, attrs, defStyleAttr, defStyleRes);
        init(context, attrs, defStyleAttr, defStyleRes);
    }

    public void init(Context context, AttributeSet attrs, int defStyleAttr, int defStyleRes) {
        TypedArray a = context.obtainStyledAttributes(attrs, R.styleable.FixedSwitchPreference, defStyleAttr, defStyleRes);
        setSummaryOn(a.getString(R.styleable.FixedSwitchPreference_summaryOn));
        setSummaryOff(a.getString(R.styleable.FixedSwitchPreference_summaryOff));
        setSwitchTextOn(a.getString(R.styleable.FixedSwitchPreference_switchTextOn));
        setSwitchTextOff(a.getString(R.styleable.FixedSwitchPreference_switchTextOff));
        setDisableDependentsState(a.getBoolean(R.styleable.FixedSwitchPreference_disableDependentsState, false));
        a.recycle();
    }

    @Override
    protected void onBindView(View view) {
        super.onBindView(view);

        View checkableView = view.findViewById(R.id.switchWidget);
        if (checkableView != null && checkableView instanceof Checkable) {
            if (checkableView instanceof SwitchCompat) {
                final SwitchCompat switchView = (SwitchCompat) checkableView;
                switchView.setOnCheckedChangeListener(null);
            }

            ((Checkable) checkableView).setChecked(isChecked());

            if (checkableView instanceof SwitchCompat) {
                final SwitchCompat switchView = (SwitchCompat) checkableView;
                switchView.setTextOn(mSwitchOn);
                switchView.setTextOff(mSwitchOff);
                switchView.setOnCheckedChangeListener(mListener);
            }
        }

        if (sSyncSummaryViewMethod != null) {
            try {
                sSyncSummaryViewMethod.invoke(this, view);
            } catch (IllegalAccessException e) {
                e.printStackTrace();
            } catch (InvocationTargetException e) {
                e.printStackTrace();
            }
        }
    }


    /**
     * Set the text displayed on the switch widget in the on state.
     * This should be a very short string; one word if possible.
     *
     * @param onText Text to display in the on state
     */
    public void setSwitchTextOn(CharSequence onText) {
        mSwitchOn = onText;
        notifyChanged();
    }

    /**
     * Set the text displayed on the switch widget in the off state.
     * This should be a very short string; one word if possible.
     *
     * @param offText Text to display in the off state
     */
    public void setSwitchTextOff(CharSequence offText) {
        mSwitchOff = offText;
        notifyChanged();
    }

    /**
     * Set the text displayed on the switch widget in the on state.
     * This should be a very short string; one word if possible.
     *
     * @param resId The text as a string resource ID
     */
    public void setSwitchTextOn(@StringRes int resId) {
        setSwitchTextOn(getContext().getString(resId));
    }

    /**
     * Set the text displayed on the switch widget in the off state.
     * This should be a very short string; one word if possible.
     *
     * @param resId The text as a string resource ID
     */
    public void setSwitchTextOff(@StringRes int resId) {
        setSwitchTextOff(getContext().getString(resId));
    }

    /**
     * @return The text that will be displayed on the switch widget in the on state
     */
    public CharSequence getSwitchTextOn() {
        return mSwitchOn;
    }

    /**
     * @return The text that will be displayed on the switch widget in the off state
     */
    public CharSequence getSwitchTextOff() {
        return mSwitchOff;
    }
}
```

attrs.xml

```xml
<resources>

    <declare-styleable name="FixedSwitchPreference">
        <!-- The summary for the Preference in a PreferenceActivity screen when the
             SwitchPreference is checked. If separate on/off summaries are not
             needed, the summary attribute can be used instead. -->
        <attr name="summaryOn" format="string"/>
        <!-- The summary for the Preference in a PreferenceActivity screen when the
             SwitchPreference is unchecked. If separate on/off summaries are not
             needed, the summary attribute can be used instead. -->
        <attr name="summaryOff" format="string"/>
        <!-- The text used on the switch itself when in the "on" state.
             This should be a very SHORT string, as it appears in a small space. -->
        <attr name="switchTextOn" format="string"/>
        <!-- The text used on the switch itself when in the "off" state.
             This should be a very SHORT string, as it appears in a small space. -->
        <attr name="switchTextOff" format="string"/>
        <!-- The state (true for on, or false for off) that causes dependents to be disabled. By default,
             dependents will be disabled when this is unchecked, so the value of this preference is false. -->
        <attr name="disableDependentsState" format="boolean"/>
    </declare-styleable>

</resources>
```

preference_widget_fixed_switch.xml

```xml
<android.support.v7.widget.SwitchCompat
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/switchWidget"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_gravity="center"
    android:padding="16dp"
    android:focusable="false"/>
```

调用的话就这么写

    :::xml
    <com.hippo.preference.FixedSwitchPreference
	    xmlns:app="http://schemas.android.com/apk/res-auto"
        style="?android:attr/preferenceStyle"
        android:key="xxxxxx"
        android:title="xxxxxxx"
        app:summaryOn="@string/main_save_image_auto_summary_on"
        app:summaryOff="@string/main_save_image_auto_summary_off"
        android:widgetLayout="@layout/preference_widget_fixed_switch"/>

**要注意的是**一定要加上 style="?android:attr/preferenceStyle"，这是为了保证 layout 与主题所用的一样，否则标题会变得很大。
